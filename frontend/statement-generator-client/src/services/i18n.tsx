import i18next from "i18next";
import home_eng from "../translations/eng/home.json";
import user_forms_eng from "../translations/eng/user_forms.json";
import logout_eng from "../translations/eng/logout.json";
import navigation_header_eng from "../translations/eng/navigation_header.json";
import post_generator_eng from "../translations/eng/post_generator.json";

import home_heb from "../translations/heb/home.json";
import user_forms_heb from "../translations/heb/user_forms.json";
import logout_heb from "../translations/heb/logout.json";
import navigation_header_heb from "../translations/heb/navigation_header.json";
import post_generator_heb from "../translations/heb/post_generator.json";

i18next
    .init({
    interpolation: { escapeValue: false },
    lng: 'eng',
    debug: true,
    resources: {
        eng: {
            home: home_eng,
            user_forms: user_forms_eng,
            logout: logout_eng,
            navigation_header: navigation_header_eng,
            post_generator: post_generator_eng,
        },
        heb: {
            home: home_heb,
            user_forms: user_forms_heb,
            logout: logout_heb,
            navigation_header: navigation_header_heb,
            post_generator: post_generator_heb,
        }
    }
});

export default i18next;