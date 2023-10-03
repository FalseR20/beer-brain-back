import {useParams} from "react-router-dom";
import Page from "./Page.tsx";

export default function Event() {
    const {event_id} = useParams();
    console.log(`Event ${event_id}`)
    return (
        <Page>
            <h1>Event {event_id}</h1>
        </Page>
    )
}