import i18next from "i18next";
import global_heb from "../translations/heb/global.json";
import home_eng from "../translations/eng/home.json";
import user_forms_eng from "../translations/eng/user_forms.json";
import logout_eng from "../translations/eng/logout.json";
import navigation_header_eng from "../translations/eng/navigation_header.json";
import post_generator_eng from "../translations/eng/post_generator.json";
import public_officials_eng from "../translations/eng/public_officials.json";

import global_eng from "../translations/eng/global.json";
import home_heb from "../translations/heb/home.json";
import user_forms_heb from "../translations/heb/user_forms.json";
import logout_heb from "../translations/heb/logout.json";
import navigation_header_heb from "../translations/heb/navigation_header.json";
import post_generator_heb from "../translations/heb/post_generator.json";
import public_officials_heb from "../translations/heb/public_officials.json";

i18next
    .init({
    interpolation: { escapeValue: false },
    lng: 'eng',
    debug: true,
    resources: {
        eng: {
            global: global_eng,
            home: home_eng,
            user_forms: user_forms_eng,
            logout: logout_eng,
            navigation_header: navigation_header_eng,
            post_generator: post_generator_eng,
            public_officials: public_officials_eng,
        },
        heb: {
            global: global_heb,
            home: home_heb,
            user_forms: user_forms_heb,
            logout: logout_heb,
            navigation_header: navigation_header_heb,
            post_generator: post_generator_heb,
            public_officials: public_officials_heb,
        }
    }
});

export default i18next;