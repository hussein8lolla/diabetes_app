document.addEventListener('DOMContentLoaded', function () {
    // إخفاء التنبيهات بعد 5 ثوان
    document.querySelectorAll('.alert-dismissible').forEach(alert => {
        setTimeout(() => {
            try { bootstrap.Alert.getOrCreateInstance(alert).close(); } catch(e) {}
        }, 5000);
    });

    // منع الإرسال المزدوج
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function () {
            const btn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (btn) {
                setTimeout(() => {
                    btn.disabled = true;
                    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> جارٍ المعالجة...';
                }, 10);
            }
        });
    });
});