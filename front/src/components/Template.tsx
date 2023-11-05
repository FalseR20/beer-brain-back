import { ReactNode } from "react";
import "../css/Template.css";
import { isAuthorized } from "../authentication.ts";
import Guest from "./Guest.tsx";
import Header from "./Header.tsx";

interface PageProps {
  children?: ReactNode;
  isAuthRequired?: boolean;
}

export default function Template(props: PageProps) {
  const inner: ReactNode =
    props.isAuthRequired == true && !isAuthorized() ? Guest() : props.children;
  return (
    <>
      <div className={"d-flex flex-column min-vh-100"}>
        <Header />
        <div className={"d-flex flex-row justify-content-center flex-grow-1"}>
          <div id={"common-field"} className={"width-60 m-3"}>
            {inner}
          </div>
        </div>
        <footer className="bg-body-tertiary border-top text-center text-white-50 p-2">
          &copy; FalseR / Bebra Bebrou
        </footer>
      </div>
    </>
  );
}
