import { IChatElement } from "./interfaces.ts";
import { ListGroup } from "react-bootstrap";
import { Avatar48 } from "../Profile.tsx";

export function EventChatBody() {
  const chatElements: IChatElement[] = [{
    member: {
      id: 1, name_letters: "U1",
    }, action: "Initialed", datetime: "2023-10-30 12:00:00",
  }, {
    member: {
      id: 2, name_letters: "U2",
    }, action: "Added money", datetime: "2023-10-30 12:01:00",
  }, {
    member: {
      id: 3, name_letters: "UT",
    }, action: "Added money", datetime: "2023-10-30 12:01:00",
  }];
  return (<>
    <ListGroup variant={"flush"} className={"p-0"}>
      {chatElements.map(chatElement => (
        <ListGroup.Item className={"d-flex flex-row border-0"} key={chatElement.datetime}>
          <Avatar48 id={chatElement.member.id} />
          <div className={"bg-body-tertiary flex-grow-1 rounded rounded-3 my-0"}>
            {/*{chatElement.action}*/}
          </div>
        </ListGroup.Item>))}
    </ListGroup>
  </>);
}