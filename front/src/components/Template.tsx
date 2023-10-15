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
      <Header />
      <div id={"common-field"} className={"mx-auto width-60"}>
        {inner}
      </div>
    </>
  );
}
