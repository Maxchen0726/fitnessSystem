// 全局JavaScript功能

// 自动关闭警告消息
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });
    
    // 初始化所有工具提示
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // 为动态表单添加事件监听
    setupDynamicForms();
});

// 动态表单处理
function setupDynamicForms() {
    // 查找所有具有 .add-form-row 类的按钮
    const addButtons = document.querySelectorAll('.add-form-row');
    if (addButtons.length > 0) {
        addButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                addFormRow(this);
            });
        });
    }
    
    // 初始删除按钮事件
    document.querySelectorAll('.delete-form-row').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            deleteFormRow(this);
        });
    });
}

// 添加表单行
function addFormRow(button) {
    const formsetContainer = button.closest('.formset-container');
    const totalForms = formsetContainer.querySelector('[name$="-TOTAL_FORMS"]');
    const formCopyTarget = formsetContainer.querySelector('.form-rows');
    
    const currentFormCount = parseInt(totalForms.value);
    const newForm = formsetContainer.querySelector('.empty-form').cloneNode(true);
    
    newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, currentFormCount);
    newForm.classList.remove('empty-form');
    newForm.classList.add('form-row');
    newForm.style.display = 'block';
    
    formCopyTarget.appendChild(newForm);
    totalForms.value = currentFormCount + 1;
    
    // 为新添加的删除按钮添加事件
    newForm.querySelectorAll('.delete-form-row').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            deleteFormRow(this);
        });
    });
}

// 删除表单行
function deleteFormRow(button) {
    const formRow = button.closest('.form-row');
    const deleteInput = formRow.querySelector('[name$="-DELETE"]');
    
    if (deleteInput) {
        deleteInput.checked = true;
        formRow.style.display = 'none';
    } else {
        formRow.remove();
    }
}