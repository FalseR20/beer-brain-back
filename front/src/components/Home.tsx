import Page from "./Page.tsx";
import "./Home.css"

function Home() {
    return (
        <Page isAuthRequired={true}>
            <p>Active debts</p>
            <Debts/>
            <p>Closed debts</p>
        </Page>

    )
}

function Debts() {
    return (
        <>
            <div id={"debts-div"}>
                <Debt/>
            </div>
        </>
    )
}


function Debt() {
    return (
        <div className={"debt-div"}>
            <div className={"debt-top"}>
                <div className={"debt-description"}>
                    <p>Зачилка в бане</p>
                </div>
                <div className={"debt-value"}>
                    <p>+60.41</p>
                </div>
            </div>
            <div className={"debt-bottom"}>
                <div className={"debt-date"}>
                    <p>сб, 16.09</p>
                </div>
                <div className={"debt-status"}>
                    <p>Вернули 3 из 5</p>
                </div>
            </div>

        </div>
    )
}


export default Home
