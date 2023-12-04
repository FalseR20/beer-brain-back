import { IChatElement } from "./interfaces.ts";
import { ListGroup } from "react-bootstrap";
import { Avatar48 } from "../Profile.tsx";

export function EventChatBody() {
  const chatElements: IChatElement[] = [{
    member: {
      id: 1, name_letters: "U1",
    }, actions: [{ name: "Initialed", datetime: "2023-10-30 12:00:00" }],
  }, {
    member: {
      id: 2, name_letters: "U2",
    }, actions: [{
      name: "Added money", datetime: "2023-10-30 12:01:00",
    }, {
      name: "Added money", datetime: "2023-10-30 12:01:00",
    }],
  }];
  return (<>
    <ListGroup variant={"flush"}>
      {chatElements.map((chatElement, index) => (// Remove index key
        <ListGroup.Item className={"d-flex flex-row border-0 px-2 pb-2"} key={index}>
          <div className={"me-3 align-self-end"}>
            <Avatar48 id={chatElement.member.id} />
          </div>
          <div className={"flex-grow-1"}>
            {chatElement.actions.map((action, index) => (<>
              <div className={"bg-body-tertiary  rounded rounded-3 mt-2 p-2"}>
                {index == 0 ? <div>{chatElement.member.name_letters}</div> : <></>}
                {action.name} - {action.datetime}
              </div>
            </>))}
          </div>
        </ListGroup.Item>))}
    </ListGroup>
  </>);
}