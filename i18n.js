(function () {
    const translations = {
        'Karibu tena! Tafadhali ingiza taarifa zako.': 'Welcome back! Please enter your details.',
        'Barua Pepe (Email)': 'Email address',
        'Nenosiri (Password)': 'Password',
        'Umesahau nenosiri?': 'Forgot password?',
        'Ingia Kwenye Mfumo': 'Sign in',
        'Barua pepe ya akaunti': 'Account email',
        'Tengeneza token ya kubadilisha nenosiri': 'Get password reset token',
        'Rudi kwenye kuingia': 'Back to sign in',
        'Token ya kubadilisha nenosiri': 'Password reset token',
        'Nenosiri jipya': 'New password',
        'Badilisha nenosiri': 'Reset password',
        'Huna akaunti bado?': "Don't have an account?",
        'Jisajili hapa': 'Register here',
        'Jisajili - Nginap Guest House': 'Register - Nginap Guest House',
        'Ingia - Nginap Guest House': 'Sign in - Nginap Guest House',
        'Fungua akaunti mpya ya usimamizi.': 'Create a new management account.',
        'Jina Kamili': 'Full name',
        'Jina lako kamili': 'Your full name',
        'Fungua Akaunti': 'Create account',
        'Una akaunti tayari?': 'Already have an account?',
        'Ingia hapa': 'Sign in here',
        'Akaunti imefunguliwa kwa mafanikio. Tafadhali ingia.': 'Account created successfully. Please sign in.',
        'Token ya majaribio imejazwa. Weka nenosiri jipya hapa chini.': 'A test token has been filled in. Enter your new password below.',
        'Unaweza kuingia sasa.': 'You can sign in now.',
        'Usimamizi wa Guest House - Nginap': 'Guest House Management - Nginap',
        'MENYU KUU': 'MAIN MENU',
        'Muhtasari': 'Overview',
        'Booking mpya': 'New booking',
        'Booking za hivi karibuni': 'Recent bookings',
        'Muhtasari wa nafasi zilizowekwa': 'A summary of reservations',
        'Tazama zote': 'View all',
        'Hali ya vyumba vyako kwa sasa': 'Current room status',
        'Simamia vyumba': 'Manage rooms',
        'Booking': 'Bookings',
        'Fuatilia nafasi na malazi ya wageni.': 'Track guest reservations and stays.',
        'MGENI': 'GUEST',
        'CHUMBA': 'ROOM',
        'KUINGIA / KUTOKA': 'CHECK-IN / CHECK-OUT',
        'JUMLA': 'TOTAL',
        'HALI': 'STATUS',
        'KITENDO': 'ACTION',
        'Hali zote': 'All statuses',
        'Chuja booking kwa hali': 'Filter bookings by status',
        'Chuja vyumba kwa hali': 'Filter rooms by status',
        'Fungua menyu': 'Open menu',
        'Funga menyu': 'Close menu',
        'Open menu': 'Open menu',
        'Close menu': 'Close menu',
        'Tafuta mgeni au chumba...': 'Search guest or room...',
        'Hakuna booking inayolingana na utafutaji.': 'No bookings match your search.',
        'Vyumba': 'Rooms',
        'Ongeza vyumba na sasisha taarifa zake.': 'Add rooms and update their details.',
        'Ongeza chumba': 'Add room',
        'Tafuta namba au aina ya chumba...': 'Search room number or type...',
        'Vyumba vyote': 'All rooms',
        'Vilivyo wazi': 'Available',
        'Vilivyochukuliwa': 'Occupied',
        'Hakuna chumba kinacholingana na utafutaji.': 'No rooms match your search.',
        'Wageni': 'Guests',
        'WATEJA': 'GUESTS',
        'Taarifa za wageni waliosajiliwa kwenye mfumo.': 'Details of guests registered in the system.',
        'Sajili mgeni': 'Add guest',
        'Tafuta jina, simu au barua pepe...': 'Search name, phone, or email...',
        'SIMU': 'PHONE',
        'BARUA PEPE': 'EMAIL',
        'KITAMBULISHO': 'ID NUMBER',
        'ANAKOTOKA': 'FROM',
        'Bado hakuna wageni waliosajiliwa.': 'No guests have been registered yet.',
        'UCHAMBUZI': 'ANALYTICS',
        'Ripoti': 'Reports',
        'Chunguza bookings kwa siku, wiki, mwezi au mwaka.': 'Review bookings by day, week, month, or year.',
        'Pakua PDF': 'Download PDF',
        'Kipindi cha ripoti': 'Report period',
        'Siku': 'Day',
        'Wiki': 'Week',
        'Mwezi': 'Month',
        'Mwaka': 'Year',
        'Chagua tarehe': 'Choose a date',
        'Jumla ya bookings': 'Total bookings',
        'Kwa kipindi kilichochaguliwa': 'For the selected period',
        'Wageni tofauti': 'Unique guests',
        'Waliofanya booking': 'With a reservation',
        'Thamani ya booking zisizoghairiwa': 'Value of non-cancelled bookings',
        'Thamani ya nafasi, si malipo yaliyothibitishwa': 'Reservation value, not confirmed payments',
        'Booking zilizokamilika': 'Completed bookings',
        'Checkout imefanyika': 'Checked out',
        'Shughuli kwa kipindi': 'Activity by period',
        'Idadi ya booking katika kila siku au mwezi': 'Bookings per day or month',
        'Bookings za kipindi': 'Bookings in this period',
        'Rekodi zote zinazoingia kwenye tarehe ulizochagua.': 'All records that fall within your selected dates.',
        'Hakuna booking katika kipindi hiki.': 'No bookings in this period.',
        'Jumla ya vyumba': 'Total rooms',
        'Vyumba vyote': 'All rooms',
        'Vilivyosajiliwa': 'Registered',
        'Vyumba vilivyo wazi': 'Available rooms',
        'Viko tayari kupokea wageni': 'Ready for guests',
        'Booking zinazoendelea': 'Ongoing bookings',
        'Hazijafanyiwa checkout': 'Not checked out',
        'Wageni waliosajiliwa': 'Registered guests',
        'Jumla ya wageni': 'Total guests',
        'DASHBOARD': 'DASHBOARD',
        'Angalia hali ya shughuli za guest house yako.': 'Here is an overview of your guest house activity.',
        'Hujambo 👋': 'Hello 👋',
        'Habari za asubuhi 👋': 'Good morning 👋',
        'Habari za mchana 👋': 'Good afternoon 👋',
        'Habari za jioni 👋': 'Good evening 👋',
        'Habari za asubuhi': 'Good morning',
        'Habari za mchana': 'Good afternoon',
        'Habari za jioni': 'Good evening',
        'Huu hapa muhtasari wa guest house yako.': 'Here is your guest house overview.',
        'Msimamizi': 'Administrator',
        'Usimamizi': 'Management',
        'MALAZI': 'ACCOMMODATION',
        'Weka taarifa za mgeni na muda wa kukaa.': 'Enter guest details and stay dates.',
        'Weka taarifa za mawasiliano ya mgeni.': 'Enter the guest contact details.',
        'Jaza taarifa za chumba na bei ya malazi.': 'Enter the room details and nightly rate.',
        'Ongeza taarifa': 'Add details',
        'Hariri chumba': 'Edit room',
        'Hariri taarifa za mgeni': 'Edit guest details',
        'Booking mpya': 'New booking',
        'Jina kamili la mgeni': 'Guest full name',
        'Namba ya simu': 'Phone number',
        'Barua pepe (si lazima)': 'Email (optional)',
        'Namba ya kitambulisho (si lazima)': 'ID number (optional)',
        'Chumba': 'Room',
        'Tarehe ya kuingia': 'Check-in date',
        'Tarehe ya kutoka': 'Check-out date',
        'Ghairi': 'Cancel',
        'Hifadhi booking': 'Save booking',
        'Hifadhi taarifa': 'Save details',
        'Bei kwa usiku': 'Price per night',
        'Maelezo': 'Description',
        'Hali ya upatikanaji': 'Availability',
        'Kipo wazi': 'Available',
        'Kimechukuliwa': 'Occupied',
        'Anakotoka': 'Origin',
        'Anakoelekea': 'Destination',
        'Kazi': 'Occupation',
        'Futa': 'Delete',
        'Futa chumba': 'Delete room',
        'Checkout': 'Check out',
        'Mgeni ameingia': 'Checked in',
        'Imethibitishwa': 'Confirmed',
        'Imekamilika': 'Completed',
        'Imeghairiwa': 'Cancelled',
        'Inapakia ripoti...': 'Loading report...',
        'Inapakia taarifa.': 'Loading information.',
        'Inahifadhi...': 'Saving...',
        'Inatengeneza PDF...': 'Generating PDF...',
        'Hifadhi': 'Save',
        'Toka kwenye mfumo': 'Log out',
        'Usimamizi rahisi,': 'Simple management,',
        'ukarimu bora.': 'better hospitality.',
        'Mfumo wa usimamizi wa malazi': 'Guest house management system',
        'Hakuna vyumba vilivyosajiliwa bado.': 'No rooms have been registered yet.',
        'Hakuna vyumba vinavyolingana na utafutaji wako.': 'No rooms match your search.',
        'Hakuna booking zilizosajiliwa.': 'No bookings have been registered.',
        'Imeshindikana kupakia taarifa.': 'Unable to load information.',
        'Imeshindikana kupakia ripoti.': 'Unable to load report.',
        'Sajili mgeni kwanza kabla ya kutengeneza booking.': 'Register a guest before creating a booking.',
        'Hakuna chumba kilicho wazi kwa sasa.': 'No rooms are currently available.',
        'Tarehe ya kutoka lazima iwe baada ya tarehe ya kuingia.': 'The check-out date must be after the check-in date.',
        'Booking imehifadhiwa kikamilifu.': 'Booking saved successfully.',
        'Taarifa zimehifadhiwa kikamilifu.': 'Details saved successfully.',
        'Rekodi yenye historia ya booking haiwezi kufutwa.': 'Records with booking history cannot be deleted.',
        'Chumba kina historia ya booking': 'Room has booking history',
        'Mgeni ana historia ya booking': 'Guest has booking history',
        'Unathibitisha kufanya checkout ya booking hii?': 'Confirm check-out for this booking?',
        'Checkout imekamilika. Chumba sasa kipo wazi.': 'Check-out complete. The room is now available.',
        'Chagua kipindi na subiri ripoti ipakie kabla ya kupakua.': 'Choose a period and wait for the report to load before downloading.',
        'Sajili mgeni kwanza': 'Register a guest first',
        'Room ': 'Room ',
        'Chumba ': 'Room ',
        'Mgeni ': 'Guest ',
        'Mgeni': 'Guest',
        'kwa usiku': 'per night',
        'hadi ': 'to ',
        ' kwa usiku': ' per night',
        'Vyumba vyako': 'Your rooms',
        'Hakiwezi kufutwa': 'Cannot be deleted',
        'Unganisha tena': 'Reconnect',
        'Mwezi: ': 'Month: ',
        'Wiki: ': 'Week: ',
        'Siku: ': 'Day: ',
        'Mwaka: ': 'Year: ',
        'Chagua': 'Select',
        'GUEST HOUSE': 'GUEST HOUSE',
        'Hadi': 'To',
        'Haijawekwa': 'Not provided',
        'Aina ya chumba': 'Room type',
        'Namba ya chumba': 'Room number',
        'Taarifa za kina': 'Details',
        'Taarifa': 'Details',
        'TAARIFA': 'DETAILS',
        'TAARIFA ZA KINA': 'DETAILS',
        'Chagua lugha': 'Choose language',
        'Chumba ': 'Room ',
        'chumba ': 'room ',
        'Mgeni ': 'Guest ',
        'mgeni ': 'guest ',
        'kwa usiku': 'per night',
        'hadi ': 'to ',
        'Booking imehifadhiwa kwa mafanikio.': 'Booking saved successfully.',
        'Akaunti imefunguliwa kwa mafanikio. Tafadhali ingia.': 'Account created successfully. Please sign in.',
        'Imeshindikana kuunganisha na seva!': 'Could not connect to the server.',
        'Hitilafu ya mtandao!': 'Network error.',
        'Barua pepe au nenosiri sio sahihi!': 'Incorrect email or password.',
        'Imeshindikana kuthibitisha kitambulisho chako (Invalid credentials)': 'Unable to verify your credentials.',
        'Chumba hakikupatikana!': 'Room not found.',
        'Mteja hakupatikana!': 'Guest not found.',
        'Uhifadhi (Booking) haukupatikana!': 'Booking not found.',
        'Token si sahihi au muda wake umekwisha!': 'The token is invalid or has expired.',
        'Badilisha jina la guest house': 'Edit guest house name',
        'Jina la guest house': 'Guest house name',
        'TAARIFA ZA GUEST HOUSE': 'GUEST HOUSE DETAILS',
        'Jina hili litaonekana juu kushoto na litahifadhiwa kwenye kifaa hiki.': 'This name appears at the top left and is saved on this device.',
        'Hifadhi jina': 'Save name',
        'Weka jina la guest house.': 'Enter a guest house name.',
        'Jina lisizidi herufi 60.': 'The name must be 60 characters or fewer.',
        'Funga': 'Close'
    };

    const originalText = new WeakMap();
    const originalAttributes = new WeakMap();
    const storageKey = 'nginap-language';
    const originalTitle = document.title;

    function currentLanguage() {
        return localStorage.getItem(storageKey) === 'en' ? 'en' : 'sw';
    }

    function translateText(value) {
        if (currentLanguage() === 'sw') return value;
        const exact = translations[value.trim()];
        if (exact) {
            const leading = value.match(/^\s*/)[0];
            const trailing = value.match(/\s*$/)[0];
            return `${leading}${exact}${trailing}`;
        }

        return value.replace(/Chumba |chumba |Mgeni |mgeni |Msimamizi|Mwezi: |Wiki: |Siku: |Mwaka: |hadi |kwa usiku|Kipo wazi|Kimechukuliwa|Imethibitishwa|Imekamilika|Imeghairiwa|Mgeni ameingia|GUEST HOUSE|Checkout|Booking|booking|Futa/gi, (match) => translations[match] || match);
    }

    function translateNode(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            if (node.parentElement?.closest('[data-brand-name]')) return;
            if (!originalText.has(node)) originalText.set(node, node.nodeValue);
            const translated = translateText(originalText.get(node));
            if (node.nodeValue !== translated) node.nodeValue = translated;
            return;
        }

        if (node.nodeType !== Node.ELEMENT_NODE) return;
        for (const attribute of ['placeholder', 'aria-label', 'title']) {
            if (!node.hasAttribute(attribute)) continue;
            let originals = originalAttributes.get(node);
            if (!originals) {
                originals = {};
                originalAttributes.set(node, originals);
            }
            if (!(attribute in originals)) originals[attribute] = node.getAttribute(attribute);
            const translated = translateText(originals[attribute]);
            if (node.getAttribute(attribute) !== translated) node.setAttribute(attribute, translated);
        }

        if (node.tagName === 'OPTION') {
            let originals = originalAttributes.get(node);
            if (!originals) {
                originals = {};
                originalAttributes.set(node, originals);
            }
            if (!('optionText' in originals)) originals.optionText = node.textContent;
            const translated = translateText(originals.optionText);
            if (node.textContent !== translated) node.textContent = translated;
        }

        node.childNodes.forEach(translateNode);
    }

    function applyLanguage(language) {
        localStorage.setItem(storageKey, language);
        document.documentElement.lang = language;
        translateNode(document.body);
        document.querySelectorAll('[data-language-switch]').forEach((select) => {
            select.value = language;
            select.setAttribute('aria-label', language === 'en' ? 'Choose language' : 'Chagua lugha');
        });
        const menuToggle = document.getElementById('menu-toggle');
        if (menuToggle) {
            const isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
            menuToggle.setAttribute('aria-label', language === 'en'
                ? (isOpen ? 'Close menu' : 'Open menu')
                : (isOpen ? 'Funga menyu' : 'Fungua menyu'));
        }
        document.title = language === 'en' ? translateText(originalTitle) : originalTitle;
    }

    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('[data-language-switch]').forEach((select) => {
            select.addEventListener('change', () => applyLanguage(select.value));
        });

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'characterData') {
                    translateNode(mutation.target);
                } else {
                    mutation.addedNodes.forEach(translateNode);
                }
            });
        });
        observer.observe(document.body, { childList: true, characterData: true, subtree: true });
        applyLanguage(currentLanguage());
    });

    window.setAppLanguage = applyLanguage;
    window.getAppLanguage = currentLanguage;
})();
