import { Text, Group } from "@mantine/core";
import { use } from "chai";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { ChangeLanguageToggle } from "../ChangeLanguageFooter/ChangeLanguageFooter";
interface NavLinkProps {
  href: string;
  label: string;
  currentRoute: string;
}

const NavLink: React.FC<NavLinkProps> = ({ href, label, currentRoute }) => (
  <Text
    c={currentRoute === href ? 'blue' : 'dimmed'}
    fw={currentRoute === href ? 'bold' : 'normal'}
  >
    <Link to={href}>{label}</Link>
  </Text>
);

export function NavigationHeader({route}: {route: string}) {
    const { t, i18n } = useTranslation("navigation_header");
    return (
      <Group justify="center" mt="xl" mb="md">
        <NavLink href="/generate" label={t("generate_page")} currentRoute={route} />
        <NavLink href="/history" label={t("history_page")} currentRoute={route} />
        <NavLink href="/profile" label={t("profile_page")} currentRoute={route} />
        <NavLink href="/public-officials" label={t("public_officials_page")} currentRoute={route} />
        <NavLink href="/logout" label={t("logout_page")} currentRoute={route} />
      </Group>
    );
}