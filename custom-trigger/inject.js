(function() {
    const button = document.createElement('button');
    button.innerHTML = 'Testplan generator';
    button.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 10000;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 25px;
        border-radius: 50px;
        cursor: pointer;
        font-family: Arial, sans-serif;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s;
        border: 2px solid white;
    `;
    
    button.onmouseover = function() {
        this.style.transform = 'scale(1.05)';
        this.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.6)';
    };
    
    button.onmouseout = function() {
        this.style.transform = 'scale(1)';
        this.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
    };
    
    button.onclick = function() {
        if (document.getElementById('test-search-modal')) {
            return;
        }
        
        const modal = document.createElement('div');
        modal.id = 'test-search-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 10001;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 0;
            transition: opacity 0.3s;
        `;
        
        const iframe = document.createElement('iframe');
        iframe.src = './custom-trigger/index.html';
        iframe.sandbox = 'allow-scripts allow-top-navigation allow-top-navigation-by-user-activation allow-forms allow-popups allow-modals';
        iframe.style.cssText = `
            width: 90%;
            height: 90%;
            max-width: 1200px;
            border: none;
            border-radius: 12px;
            background: white;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        `;
        
        const closeBtn = document.createElement('div');
        closeBtn.innerHTML = '×';
        closeBtn.style.cssText = `
            position: absolute;
            top: 20px;
            right: 30px;
            font-size: 50px;
            color: white;
            cursor: pointer;
            font-weight: bold;
            z-index: 10002;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        `;
        closeBtn.onclick = function() {
            modal.style.opacity = '0';
            setTimeout(() => {
                if (modal.parentNode) {
                    document.body.removeChild(modal);
                }
            }, 300);
        };
        
        modal.appendChild(iframe);
        modal.appendChild(closeBtn);
        document.body.appendChild(modal);
        
        setTimeout(() => modal.style.opacity = '1', 10);
        
        modal.onclick = function(e) {
            if (e.target === modal) {
                closeBtn.onclick();
            }
        };
        
        window.addEventListener('message', function(event) {
            if (event.data === 'close-modal') {
                closeBtn.onclick();
            }
        });
    };
    
    document.body.appendChild(button);
    
    function checkForResults() {
        fetch('./found_tests.json')
            .then(res => res.json())
            .then(data => {
                if (data.tests && data.tests.length > 0) {
                    const notification = document.createElement('div');
                    notification.style.cssText = `
                        position: fixed;
                        bottom: 100px;
                        right: 20px;
                        background: #4CAF50;
                        color: white;
                        padding: 10px 20px;
                        border-radius: 8px;
                        font-family: Arial, sans-serif;
                        z-index: 9999;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                        animation: slideIn 0.3s;
                    `;
                    notification.innerHTML = `Tests found: ${data.tests.length}`;
                    document.body.appendChild(notification);
                    setTimeout(() => notification.remove(), 5000);
                }
            })
            .catch(() => {});
    }
    setTimeout(checkForResults, 1000);
})();