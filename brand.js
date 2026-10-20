(function () {
    const storageKey = 'nginap-guest-house-name';
    const defaultName = 'nginap';

    function currentName() {
        return localStorage.getItem(storageKey) || defaultName;
    }

    function updateBrand(name) {
        document.querySelectorAll('[data-brand-name]').forEach((element) => {
            element.textContent = name;
        });
        document.querySelectorAll('[data-brand-mark]').forEach((element) => {
            element.textContent = name.charAt(0).toUpperCase();
        });
        document.querySelectorAll('[data-open-brand-dialog]').forEach((button) => {
            button.title = window.getAppLanguage?.() === 'en' ? 'Edit guest house name' : 'Badilisha jina la guest house';
            button.setAttribute('aria-label', button.title);
        });
    }

    function openDialog() {
        const dialog = document.getElementById('brand-dialog');
        const input = document.getElementById('brand-name-input');
        const message = document.getElementById('brand-name-message');
        input.value = currentName();
        message.textContent = '';
        dialog.showModal();
        input.focus();
        input.select();
    }

    function saveBrandName(event) {
        event.preventDefault();
        const input = document.getElementById('brand-name-input');
        const message = document.getElementById('brand-name-message');
        const name = input.value.trim().replace(/\s+/g, ' ');
        if (!name) {
            message.textContent = window.getAppLanguage?.() === 'en'
                ? 'Enter a guest house name.'
                : 'Weka jina la guest house.';
            input.focus();
            return;
        }

        if (name.length > 60) {
            message.textContent = window.getAppLanguage?.() === 'en'
                ? 'The name must be 60 characters or fewer.'
                : 'Jina lisizidi herufi 60.';
            input.focus();
            return;
        }

        localStorage.setItem(storageKey, name);
        updateBrand(name);
        document.getElementById('brand-dialog').close();
    }

    document.body.insertAdjacentHTML('beforeend', `
        <dialog id="brand-dialog" class="booking-dialog brand-dialog">
            <form id="brand-name-form">
                <div class="dialog-heading">
                    <div>
                        <span class="eyebrow">TAARIFA ZA GUEST HOUSE</span>
                        <h2 data-brand-dialog-title>Badilisha jina la guest house</h2>
                        <p data-brand-dialog-description>Jina hili litaonekana juu kushoto na litahifadhiwa kwenye kifaa hiki.</p>
                    </div>
                    <button class="dialog-close" type="button" data-close-brand-dialog aria-label="Funga">×</button>
                </div>
                <div class="input-group">
                    <label for="brand-name-input" data-brand-name-label>Jina la guest house</label>
                    <input id="brand-name-input" name="brand_name" type="text" maxlength="60" autocomplete="organization" required>
                </div>
                <p id="brand-name-message" class="msg" role="alert"></p>
                <div class="dialog-actions">
                    <button class="filter-btn" type="button" data-close-brand-dialog>Ghairi</button>
                    <button class="btn-create" type="submit" data-brand-save>Hifadhi jina</button>
                </div>
            </form>
        </dialog>
    `);

    document.querySelectorAll('[data-open-brand-dialog]').forEach((button) => {
        button.addEventListener('click', openDialog);
    });
    document.querySelectorAll('[data-close-brand-dialog]').forEach((button) => {
        button.addEventListener('click', () => document.getElementById('brand-dialog').close());
    });
    document.getElementById('brand-name-form').addEventListener('submit', saveBrandName);
    updateBrand(currentName());
    window.addEventListener('storage', (event) => {
        if (event.key === storageKey) updateBrand(currentName());
    });
})();
