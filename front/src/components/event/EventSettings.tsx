import { Button, ListGroup } from "react-bootstrap";

export function EventSettings() {
  return (<>
    <h3 className={"mt-4 mb-2"}> Danger Zone </h3>
    <ListGroup className={"border border-danger rounded-2"} variant={"flush"}>
      <ListGroup.Item className={"d-flex flex-row align-items-center"}>
        <span className={"flex-grow-1"}>Leave this event</span>
        <Button variant={"danger"} className={"my-2"}>
          {" "}
          Leave{" "}
        </Button>
      </ListGroup.Item>
      <ListGroup.Item
        className={"d-flex flex-row justify-content-between align-items-center"}
      >
        <span className={"flex-grow-1"}>Delete this event</span>
        <Button variant={"danger"} className={"my-2"}>
          {" "}
          Delete event{" "}
        </Button>
      </ListGroup.Item>
    </ListGroup>
  </>);
}