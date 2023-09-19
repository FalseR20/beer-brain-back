import {ReactNode} from "react";
import "./Page.css"
import {Link} from "react-router-dom";


interface PageProps {
    children: ReactNode;
}

function Page({children}: PageProps) {
    return (
        <div>
            <header>
                <div>
                    <Link id={"project-name"} className={"nav-sign"} to={"/"}>BeerBrain</Link>
                    <nav>
                        <Link className={"nav-sign"} to={"/sign_in"}>Sign In</Link>
                        <Link className={"nav-sign"} to={"/sign_up"}>Sign Up</Link>
                    </nav>
                </div>
            </header>
            <div id={"common-field"}>
                {children}
            </div>
            {/*<footer>*/}
            {/*    <h4>*/}
            {/*        BeerBrain 2023 (c) FalseR*/}
            {/*    </h4>*/}
            {/*</footer>*/}
        </div>
    );
}

export default Page;