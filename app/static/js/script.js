const fileUploadArea = document.getElementById('fileUploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const removeFileBtn = document.getElementById('removeFile');
const emailTextarea = document.getElementById('emailText');
const charCount = document.getElementById('charCount');
const classifyBtn = document.getElementById('classifyBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const resultsSection = document.getElementById('resultsSection');
const classificationBadge = document.getElementById('classificationBadge');
const classificationDescription = document.getElementById('classificationDescription');
const responseText = document.getElementById('responseText');
const originalText = document.getElementById('originalText');
const copyResponseBtn = document.getElementById('copyResponseBtn');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const originalTextHeader = document.getElementById('originalTextHeader');
const originalTextContent = document.getElementById('originalTextContent');
const emailForm = document.getElementById('emailForm');

let selectedFile = null;

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
        
        clearFormData();
    });
});

fileUploadArea.addEventListener('click', () => {
    fileInput.click();
});

fileUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadArea.classList.add('dragover');
});

fileUploadArea.addEventListener('dragleave', () => {
    fileUploadArea.classList.remove('dragover');
});

fileUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelection(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        selectedFile = e.target.files[0];
        handleFileSelection(selectedFile);
    }
});

removeFileBtn.addEventListener('click', () => {
    clearFileSelection();
});

function handleFileSelection(file) {
    const validTypes = ['text/plain', 'application/pdf'];
    
    if (!validTypes.includes(file.type)) {
        showNotification('Formato de arquivo não suportado. Use .txt ou .pdf', 'error');
        return;
    }
    
    if (file.size > 16 * 1024 * 1024) {
        showNotification('Arquivo muito grande. Tamanho máximo: 16MB', 'error');
        return;
    }
    
    selectedFile = file;
    fileName.textContent = file.name;
    fileUploadArea.style.display = 'none';
    fileInfo.style.display = 'block';
}

function clearFileSelection() {
    fileInput.value = '';
    selectedFile = null;
    fileName.textContent = '';
    fileUploadArea.style.display = 'block';
    fileInfo.style.display = 'none';
}

emailTextarea.addEventListener('input', () => {
    const count = emailTextarea.value.length;
    charCount.textContent = count.toLocaleString();
    
    if (count > 5000) {
        charCount.style.color = '#dc3545';
    } else if (count > 3000) {
        charCount.style.color = '#ffc107';
    } else {
        charCount.style.color = '#666';
    }
});

emailForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    const activeTab = document.querySelector('.tab-btn.active').dataset.tab;
    
    if (activeTab === 'file') {
        const fileToUpload = selectedFile || (fileInput.files && fileInput.files[0]);
        if (!fileToUpload) {
            showNotification('Por favor, selecione um arquivo', 'error');
            return;
        }
        formData.append('file', fileToUpload);
    } else {
        const emailText = emailTextarea.value.trim();
        if (!emailText) {
            showNotification('Por favor, digite o conteúdo do email', 'error');
            return;
        }
        if (emailText.length < 10) {
            showNotification('O texto do email deve ter pelo menos 10 caracteres', 'error');
            return;
        }
        formData.append('email_text', emailText);
    }
    
    showLoading(true);
    classifyBtn.disabled = true;
    
    try {
        const response = await fetch('/classify', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Erro na classificação');
        }
        
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        showNotification(error.message || 'Erro ao processar email', 'error');
    } finally {
        showLoading(false);
        classifyBtn.disabled = false;
    }
});

function displayResults(result) {
    const isProductive = result.classification === 'Produtivo';
    classificationBadge.textContent = result.classification;
    classificationBadge.className = `classification-badge ${isProductive ? 'productive' : 'unproductive'}`;
    
    classificationDescription.textContent = isProductive 
        ? 'Este email requer ação ou resposta específica'
        : 'Este email não necessita de ação imediata';
    
    responseText.textContent = result.response;
    
    originalText.textContent = result.original_text;
    
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    originalTextContent.classList.remove('expanded');
    originalTextHeader.classList.remove('expanded');
}

copyResponseBtn.addEventListener('click', async () => {
    try {
        await navigator.clipboard.writeText(responseText.textContent);
        showNotification('Resposta copiada para a área de transferência!', 'success');
        
        const originalText = copyResponseBtn.innerHTML;
        copyResponseBtn.innerHTML = '<i class="fas fa-check"></i> Copiado!';
        setTimeout(() => {
            copyResponseBtn.innerHTML = originalText;
        }, 2000);
        
    } catch (error) {
        console.error('Error copying text:', error);
        showNotification('Erro ao copiar texto', 'error');
    }
});

originalTextHeader.addEventListener('click', () => {
    const isExpanded = originalTextContent.classList.contains('expanded');
    
    if (isExpanded) {
        originalTextContent.classList.remove('expanded');
        originalTextHeader.classList.remove('expanded');
        originalTextHeader.querySelector('span').textContent = 'Visualizar texto original';
    } else {
        originalTextContent.classList.add('expanded');
        originalTextHeader.classList.add('expanded');
        originalTextHeader.querySelector('span').textContent = 'Ocultar texto original';
    }
});

newAnalysisBtn.addEventListener('click', () => {
    resultsSection.style.display = 'none';
    clearFormData();
    document.querySelector('.upload-section').scrollIntoView({ behavior: 'smooth' });
});

function showLoading(show) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
}

function clearFormData() {
    clearFileSelection();
    selectedFile = null;
    emailTextarea.value = '';
    charCount.textContent = '0';
    charCount.style.color = '#666';
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
        <button class="notification-close">&times;</button>
    `;
    
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '15px 20px',
        borderRadius: '5px',
        color: 'white',
        zIndex: '1001',
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        maxWidth: '400px',
        fontSize: '14px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
        animation: 'slideIn 0.3s ease'
    });
    
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };
    notification.style.background = colors[type] || colors.info;
    
    document.body.appendChild(notification);
    
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.style.cssText = 'background: none; border: none; color: white; font-size: 18px; cursor: pointer; margin-left: auto;';
    closeBtn.addEventListener('click', () => {
        notification.remove();
    });
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || icons.info;
}

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (!classifyBtn.disabled) {
            emailForm.dispatchEvent(new Event('submit'));
        }
    }
    
    if (e.key === 'Escape' && resultsSection.style.display !== 'none') {
        newAnalysisBtn.click();
    }
});