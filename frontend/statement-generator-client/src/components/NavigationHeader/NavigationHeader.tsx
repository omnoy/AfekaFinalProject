import { Text, Group } from "@mantine/core";
import { Link } from "react-router-dom";
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

    return (
        <Group justify="center" mt="xl" mb="md">
      <NavLink href="/generate" label="Generate Post" currentRoute={route} />
      <NavLink href="/history" label="Post History" currentRoute={route} />
      <NavLink href="/profile" label="User Profile" currentRoute={route} />
      <NavLink href="/logout" label="Logout" currentRoute={route} />
    </Group>
    );
}