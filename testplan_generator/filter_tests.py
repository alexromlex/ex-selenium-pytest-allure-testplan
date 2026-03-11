
from typing import Dict, List, Any, Union

class TestFilter:
    def __init__(self, data: Dict):
        self.tests = data
    
    def filter(self, filters: Union[Dict, List]) -> List[Dict]:
        if isinstance(filters, list):
            results = []
            seen_ids = set()
            
            for single_filter in filters:
                filtered = self._strict_filter(single_filter)
                for test in filtered:
                    if test['id'] not in seen_ids:
                        seen_ids.add(test['id'])
                        results.append(test)
            return results

        return self._strict_filter(filters)
    
    def _strict_filter(self, filters: Dict) -> List[Dict]:
        if not isinstance(filters, dict):
            return []
            
        result = []
        for test in self.tests:
            if self._match_strict(test, filters):
                result.append(test)
        return result
    
    def _match_strict(self, test: Dict, filters: Dict) -> bool:
        for field, condition in filters.items():
            if field == 'id':
                if not self._evaluate(test.get('id'), condition):
                    return False
                    
            elif field == 'name':
                if not self._evaluate(test.get('name'), condition):
                    return False
                    
            elif field == 'markers':
                if not self._evaluate(test.get('markers', []), condition):
                    return False
                    
            elif field == 'labels':
                for label_key, label_condition in condition.items():
                    value = None
                    for label in test.get('labels', []):
                        if label_key in label:
                            value = label[label_key]
                            break
                    
                    if not self._evaluate(value, label_condition):
                        return False
            else:
                return False
        
        return True
    
    def _evaluate(self, value: Any, condition: Dict) -> bool:
        for op, target in condition.items():
            if op == 'eq':
                return value == target
            elif op == 'neq':
                return value != target
            elif op == 'in':
                if value is None:
                    return False
                if isinstance(value, list):
                    return any(v in target for v in value)
                return value in target
            elif op == 'nin':
                if value is None:
                    return True
                if isinstance(value, list):
                    return not any(v in target for v in value)
                return value not in target
            elif op == 'exists':
                return (value is not None) == target
        return False
