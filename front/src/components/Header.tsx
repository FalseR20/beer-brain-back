import { Button, Navbar } from "react-bootstrap";
import { isAuthorized, signOut } from "../authentication.ts";
import { ThemeContext } from "../themeContext.tsx";
import { BsMoon, BsSun } from "react-icons/bs";

export default function Header() {
  return (
    <header className="d-flex flex-row justify-content-center bg-body-tertiary">
      <Navbar
        className={
          "d-flex flex-row justify-content-between align-items-center width-60"
        }
      >
        <Navbar.Brand href={"/"} className={"fs-3"}>
          BeerBrain
        </Navbar.Brand>
        <Navbar.Collapse className={"justify-content-end"}>
          <SignGroup />
          <ThemeSwitcher />
        </Navbar.Collapse>
      </Navbar>
    </header>
  );
}

export function ThemeSwitcher() {
  return (
    <>
      <ThemeContext.Consumer>
        {({ isDark, switchTheme }) => (
          <a
            className={"fs-2 text-body pb-2 hover-cursor-pointer"}
            onClick={switchTheme}
          >
            {isDark ? <BsSun /> : <BsMoon />}
          </a>
        )}
      </ThemeContext.Consumer>
    </>
  );
}

export function SignGroup() {
  return isAuthorized() ? (
    <>
      <Button
        variant={"outline-secondary"}
        className={"me-3"}
        onClick={() => {
          signOut();
          window.location.replace("/");
        }}
      >
        Sign Out
      </Button>
    </>
  ) : (
    <>
      <Button variant={"outline-success"} className={"me-3"} href={"/sign_in"}>
        Sign In
      </Button>
      <Button variant={"success"} className={"me-3"} href={"/sign_up"}>
        Sign Up
      </Button>
    </>
  );
}
