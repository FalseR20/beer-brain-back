import {useParams} from "react-router-dom";
import Page from "./Page.tsx";
import {useEffect, useState} from "react";
import NotFound from "./NotFound.tsx";
import getAuthHeader from "../authentication.ts";

interface IEvent {
    id: number,
    date: string,
    description: string,
    is_closed: boolean,
    members: [
        {
            id: number,
            user: number,
            event: number,
            deposits: [
                {
                    id: number,
                    description: string,
                    value: number,
                }
            ]
        },
    ]

}


export default function Event() {
    const params = useParams();
    const event_id = parseInt(params.event_id as string)
    if (isNaN(event_id)) {
        return <NotFound/>
    }
    return EventValidated(event_id)
}

function EventValidated(event_id: number) {
    const [event, setEvent] = useState<IEvent | undefined>(undefined);
    useEffect(
        () => {
            fetch(`http://127.0.0.1:8000/core/events/${event_id}`, {
                headers: getAuthHeader(),
            }).then(response => response.json())
                .then(data => {
                    setEvent(data)
                    console.log(data)
                });
        }, [event_id]
    )


    if (event == undefined) {
        return (
            <Page/>
        )
    }

    return (
        <Page>
            <h1>Event {event.description}</h1>
            <h2>Event info:</h2>
            <code style={{"whiteSpace": "break-spaces"}}>{JSON.stringify(event, null, 3)}</code>
        </Page>
    )
}