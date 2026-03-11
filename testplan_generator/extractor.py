import ast
import os
import configparser
from pathlib import Path
from typing import Dict, List, Any, Set, Optional


class AllureValueTransformer:
    
    @staticmethod
    def get_value(node: ast.AST) -> str:
        if isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            if hasattr(node, 'value') and hasattr(node.value, 'id') and node.value.id == 'allure':
                if node.attr == 'severity_level':
                    return ''
            value = AllureValueTransformer.get_value(node.value)
            return f"{value}.{node.attr}" if value else node.attr
        elif isinstance(node, ast.Call):
            if node.args:
                return AllureValueTransformer.get_value(node.args[0])
            elif node.keywords:
                for kw in node.keywords:
                    if kw.arg == 'value':
                        return AllureValueTransformer.get_value(kw.value)
            func_name = AllureValueTransformer.get_value(node.func)
            return func_name
        elif isinstance(node, ast.List):
            values = [AllureValueTransformer.get_value(elt) for elt in node.elts]
            return ','.join(values)
        elif isinstance(node, ast.Tuple):
            values = [AllureValueTransformer.get_value(elt) for elt in node.elts]
            return ','.join(values)
        elif node is None:
            return ''
        
        return ''


class AllureLabelExtractor(ast.NodeVisitor):
    """Exctractor from @allure decorators"""
    
    def __init__(self):
        self.labels: List[Dict[str, str]] = []
        self.test_id: str = ''
        
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for decorator in node.decorator_list:
            self._process_decorator(decorator)
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for decorator in node.decorator_list:
            self._process_decorator(decorator)
    
    def _process_decorator(self, decorator: ast.AST) -> None:
        if isinstance(decorator, ast.Call) and hasattr(decorator.func, 'attr'):
            if hasattr(decorator.func, 'value') and hasattr(decorator.func.value, 'id'):
                if decorator.func.value.id == 'allure':
                    label_name = decorator.func.attr
                    
                    if label_name == 'id':
                        if decorator.args:
                            self.test_id = AllureValueTransformer.get_value(decorator.args[0])
                        return
                    
                    if decorator.args:
                        value_node = decorator.args[0]
                        value = self._extract_allure_value(value_node, label_name)
                        if value:
                            self.labels.append({label_name: value})
                    elif decorator.keywords:
                        for kw in decorator.keywords:
                            value = self._extract_allure_value(kw.value, f"{label_name}.{kw.arg}")
                            if value:
                                self.labels.append({f"{label_name}.{kw.arg}": value})
        
        elif isinstance(decorator, ast.Attribute) and hasattr(decorator.value, 'id'):
            if decorator.value.id == 'allure' and decorator.attr != 'id':
                self.labels.append({decorator.attr: 'true'})
    
    def _extract_allure_value(self, value_node: ast.AST, label_name: str) -> str:
        if label_name == 'severity' and isinstance(value_node, ast.Attribute):
            if hasattr(value_node, 'attr'):
                return value_node.attr.lower()
        
        value = AllureValueTransformer.get_value(value_node)
        
        if value and 'severity_level' in value:
            parts = value.split('.')
            if parts:
                return parts[-1].lower()
        
        return value


class PytestMarkerExtractor(ast.NodeVisitor):   
    def __init__(self, allowed_markers: Set[str]):
        self.markers: List[str] = []
        self.allowed_markers = allowed_markers
        self.default_excluded = {'parametrize', 'skip', 'filterwarnings', 
                                 'skipif', 'usefixtures', 'xfail', 'run'}
        
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for decorator in node.decorator_list:
            self._process_marker(decorator)
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for decorator in node.decorator_list:
            self._process_marker(decorator)
    
    def _process_marker(self, decorator: ast.AST) -> None:
        marker_name = None
        
        if isinstance(decorator, ast.Attribute) and hasattr(decorator.value, 'attr'):
            if decorator.value.attr == 'mark' and hasattr(decorator.value.value, 'id'):
                if decorator.value.value.id == 'pytest':
                    marker_name = decorator.attr
        
        elif isinstance(decorator, ast.Call) and hasattr(decorator.func, 'attr'):
            if hasattr(decorator.func, 'value') and hasattr(decorator.func.value, 'attr'):
                if decorator.func.value.attr == 'mark' and hasattr(decorator.func.value.value, 'id'):
                    if decorator.func.value.value.id == 'pytest':
                        marker_name = decorator.func.attr
        
        if marker_name:
            self._add_marker_if_allowed(marker_name)
    
    def _add_marker_if_allowed(self, marker_name: str) -> None:
        if self.allowed_markers:
            if marker_name in self.allowed_markers and marker_name not in self.markers:
                self.markers.append(marker_name)
        else:
            if marker_name not in self.default_excluded and marker_name not in self.markers:
                self.markers.append(marker_name)


class TestCollector(ast.NodeVisitor):
    
    def __init__(self, filename: str, allowed_markers: Set[str]):
        self.filename = filename
        self.allowed_markers = allowed_markers
        self.tests: List[Dict[str, Any]] = []
        self.current_class_labels: List[Dict[str, str]] = []
        self.current_class_markers: List[str] = []
        self.current_class_id: str = ''  # id class
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        old_labels = self.current_class_labels.copy()
        old_markers = self.current_class_markers.copy()
        old_class_id = self.current_class_id
        
        # get allure lables
        class_label_extractor = AllureLabelExtractor()
        class_label_extractor.visit(node)
        self.current_class_labels.extend(class_label_extractor.labels)
        
        # get id
        if class_label_extractor.test_id:
            self.current_class_id = class_label_extractor.test_id
        
        # get markers
        class_marker_extractor = PytestMarkerExtractor(self.allowed_markers)
        class_marker_extractor.visit(node)
        self.current_class_markers.extend(class_marker_extractor.markers)
        
        self.generic_visit(node)
        
        self.current_class_labels = old_labels
        self.current_class_markers = old_markers
        self.current_class_id = old_class_id
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.name.startswith('test_'):
            test_label_extractor = AllureLabelExtractor()
            test_label_extractor.visit(node)
            
            test_id = test_label_extractor.test_id
            
            all_labels = self.current_class_labels.copy()
            
            for test_label in test_label_extractor.labels:
                key = list(test_label.keys())[0]
                all_labels = [el for el in all_labels if list(el.keys())[0] != key]
                all_labels.append(test_label)
            
            test_marker_extractor = PytestMarkerExtractor(self.allowed_markers)
            test_marker_extractor.visit(node)
            
            all_markers = list(set(self.current_class_markers + test_marker_extractor.markers))
            all_markers.sort()
            
            test_info = {
                'id': test_id,
                'name': node.name,
                'labels': all_labels,
                'markers': all_markers
            }
            
            self.tests.append(test_info)


def load_pytest_markers(pytest_ini_path: Path) -> Set[str]:
    
    markers = set()
    
    if not pytest_ini_path or not pytest_ini_path.exists():
        return markers
    
    config = configparser.ConfigParser()
    config.read(pytest_ini_path)
    
    markers_text = ''
    if 'pytest' in config and 'markers' in config['pytest']:
        markers_text = config['pytest']['markers']
    elif 'tool:pytest' in config and 'markers' in config['tool:pytest']:
        markers_text = config['tool:pytest']['markers']
    
    if markers_text:
        for line in markers_text.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                marker_name = line.split()[0].split(':')[0].strip()
                if marker_name:
                    markers.add(marker_name)
    
    return markers


def find_pytest_ini(start_path: Path) -> Optional[Path]:
    
    current_path = start_path.absolute()
    
    while current_path != current_path.parent:
        pytest_ini = current_path / 'pytest.ini'
        if pytest_ini.exists():
            return pytest_ini
        current_path = current_path.parent
    
    return None


def find_test_files(tests_dir: Path) -> List[Path]:
    
    if not tests_dir.exists():
        return []
    
    test_files = []
    for root, _, files in os.walk(tests_dir):
        for file in files:
            if file.startswith('test_') and file.endswith('.py'):
                test_files.append(Path(root) / file)
    
    return test_files


def collect_tests_info(test_files: List[Path], allowed_markers: Set[str]) -> List[Dict[str, Any]]:

    all_tests = []
    
    for test_file in test_files:
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            collector = TestCollector(str(test_file), allowed_markers)
            collector.visit(tree)
            
            all_tests.extend(collector.tests)
            
        except Exception as e:
            print(f"Error processing file {test_file}: {e}")
            continue
    
    return all_tests


def extract_test(tests_dir: str = 'tests') -> Dict[str, Any]:
    
    current_dir = Path.cwd()
    tests_path = current_dir / tests_dir
    
    print(f"Test founded in: {tests_path}")
    
    pytest_ini_path = find_pytest_ini(tests_path)
    allowed_markers = set()
    
    if pytest_ini_path:
        allowed_markers = load_pytest_markers(pytest_ini_path)
        print(f"Found pytest.ini: {pytest_ini_path}")
        print(f"Found allowed markers ({len(allowed_markers)}): {sorted(allowed_markers)}")
    else:
        print("pytest.ini not found will use default markers")
    
    test_files = find_test_files(tests_path)
    print(f"Found test files: {len(test_files)}")
    
    tests_info = collect_tests_info(test_files, allowed_markers)
    print(f"Found tests: {len(tests_info)}")
    # print(f"\n{tests_info}")
    return tests_info
