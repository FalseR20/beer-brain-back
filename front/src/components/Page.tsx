import {ReactNode} from "react";
import "../css/Page.css"
import {Link} from "react-router-dom";
import {isAuthorized, signOut} from "../authentication.ts";
import Guest from "./Guest.tsx";


interface PageProps {
    children?: ReactNode;
    isAuthRequired?: boolean;
}

function out() {
    signOut();
    window.location.replace("/");
}

function Links() {
    if (!isAuthorized()) {
        return (
            <>
                <Link className={"nav-sign"} to={"/sign_in"}>Sign In</Link>
                <Link className={"nav-sign"} to={"/sign_up"}>Sign Up</Link>
            </>
        )
    }
    return (
        <>
            <a className={"nav-sign"} onClick={out}>Sign Out</a>
        </>
    )

}

export default function Page(props: PageProps) {
    const inner: ReactNode = (props.isAuthRequired == true && !isAuthorized()) ? Guest() : props.children;
    return (
        <div>
            <header>
                <div>
                    <Link id={"project-name"} className={"nav-sign"} to={"/"}>BeerBrain</Link>
                    <nav>
                        {Links()}
                    </nav>
                </div>
            </header>
            <div id={"common-field"}>
                {inner}
            </div>
        </div>
    )
}
