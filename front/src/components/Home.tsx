import Page from "./Page.tsx";
import "./Home.css"
import {ReactNode, useEffect, useState} from "react";

export default function Home() {
    return (
        <Page isAuthRequired={true}>
            <div id={"debts-div"}>
                <p>Active debts</p>
                <Debts/>
                <p>Closed debts</p>
            </div>

        </Page>

    )
}

interface DebtJSON {
    id: number,
    members_count: number,
    date: string,
    description: string,
    is_closed: boolean
}

function Debts(): ReactNode {
    const [debts, setDebts] = useState<DebtJSON[]>([]);

    useEffect(
        () => {
            fetch("http://127.0.0.1:8000/core/common-events/", {
                headers: {
                    "Authorization": "Token 8ec432c76c8ac809f9315ba63964980f51136347"
                }
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
