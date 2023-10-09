import {ReactNode} from "react";
import "../css/Page.scss"
import {Link} from "react-router-dom";
import {isAuthorized, signOut} from "../authentication.ts";
import Guest from "./Guest.tsx";
import {ThemeContext} from "../themeContext.tsx";
import {BsMoon, BsSun} from "react-icons/bs";


interface PageProps {
    children?: ReactNode;
    isAuthRequired?: boolean;
}

function out() {
    signOut();
    window.location.replace("/");
}

function Links() {
    return (
        <>
            <ThemeContext.Consumer>
                {({isDark, switchTheme}) => (
                    <a className={"nav-sign"} onClick={switchTheme}>
                        {isDark ? <BsSun/> : <BsMoon/>}
                    </a>
                )}
            </ThemeContext.Consumer>

            {
                isAuthorized() ? (
                    <>
                        <a className={"nav-sign"} onClick={out}>Sign Out</a>
                    </>
                ) : (
                    <>

                        <Link className={"nav-sign"} to={"/sign_in"}>Sign In</Link>
                        <Link className={"nav-sign"} to={"/sign_up"}>Sign Up</Link>
                    </>
                )
            }
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
