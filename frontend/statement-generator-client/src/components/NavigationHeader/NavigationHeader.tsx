import { Anchor, Group, Title } from "@mantine/core";

interface NavLinkProps {
  href: string;
  label: string;
  currentRoute: string;
}

const NavLink: React.FC<NavLinkProps> = ({ href, label, currentRoute }) => (
  <Anchor
    href={href}
    c={currentRoute === href ? 'blue' : 'dimmed'}
    font-weight={currentRoute === href ? 'bold' : 'normal'}
  >
    {label}
  </Anchor>
);

export function NavigationHeader({route}: {route: string}) {

    return (
        <Group justify="center" mt="xl" mb="md">
      <NavLink href="/generate" label="Generate Post" currentRoute={route} />
      <NavLink href="/history" label="Post History" currentRoute={route} />
      <NavLink href="/profile" label="User Profile" currentRoute={route} />
      <NavLink href="/" label="Logout" currentRoute={route} />
    </Group>
    );
}