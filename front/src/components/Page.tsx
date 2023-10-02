import {ReactNode} from "react";
import "./Page.css"
import {Link} from "react-router-dom";
import {isAuthorized, signOut} from "../auth/authentication.ts";


interface PageProps {
    children: ReactNode;
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

export default function Page({children}: PageProps) {
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
                {children}
            </div>
        </div>
    )
        ;
}
