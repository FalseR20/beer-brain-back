import { ReactNode } from "react";
import "../css/Page.scss";
import { isAuthorized, signOut } from "../authentication.ts";
import Guest from "./Guest.tsx";
import { ThemeContext } from "../themeContext.tsx";
import { BsMoon, BsSun } from "react-icons/bs";
import { Button, Navbar } from "react-bootstrap";

interface PageProps {
  children?: ReactNode;
  isAuthRequired?: boolean;
}

export default function Page(props: PageProps) {
  const inner: ReactNode =
    props.isAuthRequired == true && !isAuthorized() ? Guest() : props.children;
  return (
    <>
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
      <div id={"common-field"} className={"mx-auto width-60"}>
        {inner}
      </div>
    </>
  );
}

function ThemeSwitcher() {
  return (
    <>
      <ThemeContext.Consumer>
        {({ isDark, switchTheme }) => (
          <a
            id={"theme-switcher"}
            className={"fs-2 text-body pb-2"}
            onClick={switchTheme}
          >
            {isDark ? <BsSun /> : <BsMoon />}
          </a>
        )}
      </ThemeContext.Consumer>
    </>
  );
}

function SignGroup() {
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
      <Button
        variant={"outline-secondary"}
        className={"me-3"}
        href={"/sign_in"}
      >
        Sign In
      </Button>
      <Button variant={"secondary"} className={"me-3"} href={"/sign_up"}>
        Sign Up
      </Button>
    </>
  );
}
