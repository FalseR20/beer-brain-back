import Page from "./Page.tsx";
import "./Home.css"
import {ReactNode, useEffect, useState} from "react";
import {Link} from "react-router-dom";
import getAuthHeader from "../auth/authentication.ts";

interface DebtJSON {
    id: number,
    members_count: number,
    date: string,
    description: string,
    is_closed: boolean
}

export default function Home() {
    return (
        <Page isAuthRequired={true}>
            <div id={"debts-div"}>
                <div className={"debt-buttons"}>
                    <Link className={"debt-button link-button"} to={"/create_event"}>Create event</Link>
                    <Link className={"debt-button link-button"} to={"/join_event"}>Join event</Link>
                </div>
                <p>All debts</p>
                <Debts/>
            </div>

        </Page>

    )
}

function Debts(): ReactNode {
    const [debts, setDebts] = useState<DebtJSON[]>([]);

    useEffect(
        () => {
            fetch("http://127.0.0.1:8000/core/common-events/", {
                headers: getAuthHeader(),
            }).then(response => response.json())
                .then(data => setDebts(data));
        }, []
    )

    return (
        <>
            {debts.map(
                (debt => Debt(debt))
            )}
        </>

    )
}


function Debt(debtJSON: DebtJSON) {
    console.log(debtJSON);
    return (
        <div key={`Debt${debtJSON.id}`} className={"debt-div"}>
            <div className={"debt-top"}>
                <div className={"debt-description"}>
                    <p>{debtJSON.description}</p>
                </div>
                <div className={"debt-value"}>
                    <p>{debtJSON.is_closed.toString()}</p>
                </div>
            </div>
            <div className={"debt-bottom"}>
                <div className={"debt-date"}>
                    <p>{debtJSON.date}</p>
                </div>
                <div className={"debt-status"}>
                    <p>{debtJSON.members_count} members</p>
                </div>
            </div>

        </div>
    )
}
