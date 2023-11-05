import { Button, Modal, Navbar } from "react-bootstrap";
import { isAuthorized, signOut } from "../authentication.ts";
import { ThemeContext } from "../themeContext.tsx";
import { BsMoon, BsSun } from "react-icons/bs";
import { useState } from "react";

export default function Header() {
  return (
    <header className="d-flex flex-row justify-content-center bg-body-tertiary border-bottom">
      <Navbar
        className={
          "width-60 mx-3 d-flex flex-row justify-content-between align-items-center"
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
  const [show, setShow] = useState(false);

  return (
    <>
      <ThemeContext.Consumer>
        {({ isDark, switchTheme }) => (
          <>
            <a
              className={"fs-2 text-body pb-2 hover-cursor-pointer"}
              onClick={() => {
                if (!isDark) {
                  switchTheme();
                } else {
                  setShow(true);
                }
              }}
            >
              {isDark ? <BsSun /> : <BsMoon />}
            </a>
            <Modal
              show={show}
              onHide={() => setShow(false)}
              backdrop="static"
              keyboard={false}
            >
              <Modal.Header>
                <Modal.Title>
                  <b>No light theme!</b>
                </Modal.Title>
              </Modal.Header>
              <Modal.Body>
                Do you really wanna use this eye destroyer? Are you sure about
                this? Are you a masochist? Do you know what progress is? This is
                not about a light theme!
                <br />
                <br />
                Do you know an app called Discord? It uses a dark theme from the
                very beginning. And do you know why people decide to turn on the
                reverse? They got lost in the settings and discovered a{" "}
                <b>fucking flashbang!</b>
              </Modal.Body>
              <Modal.Footer>
                <Button
                  id={"disagree-dark-theme"}
                  variant="outline-danger"
                  onClick={() => {
                    setShow(false);
                    switchTheme();
                  }}
                  onMouseEnter={() => {
                    const but = document.getElementById("disagree-dark-theme")!;
                    setTimeout(() => {
                      but.hidden = true;
                    }, 100);
                  }}
                >
                  Destroy my eyes
                </Button>
                <Button
                  id={"agree-dark-theme"}
                  variant="success"
                  onClick={() => {
                    setTimeout(() => setShow(false), 400);
                    document.getElementById("agree-dark-theme")!.textContent =
                      "That's right!";
                  }}
                >
                  I'll continue use dark theme
                </Button>
              </Modal.Footer>
            </Modal>
          </>
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
