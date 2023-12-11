import { IChatElement } from "./interfaces.ts";
import { ListGroup } from "react-bootstrap";
import { RoundedAvatarLink } from "../Profile.tsx";

export function EventChatBody() {
  const chatElements: IChatElement[] = [{
    member: {
      profile: {
        id: 1, firstName: "User", lastName: "1",
      },
    }, actions: [{ name: "Initialed", datetime: "2023-10-30 12:00:00" }],
  }, {
    member: {
      profile: {
        id: 2, firstName: "User", lastName: "2",
      },
    }, actions: [{
      name: "Added money", datetime: "2023-10-30 12:01:00",
    }, {
      name: "Added money", datetime: "2023-10-30 12:01:00",
    }],
  }, {
    member: {
      profile: {
        id: 3, firstName: "User", lastName: "3",
      },
    }, actions: [{ name: "Added cash", datetime: "2023-10-30 12:00:00" }],
  }];
  return (<>
    <ListGroup variant={"flush"}>
      {chatElements.map(({ member, actions }, index, // Remove index key
      ) => (<ListGroup.Item
        className={"d-flex flex-row border-0 py-0 pb-1"}
        key={index}
      >
        <RoundedAvatarLink className={"align-self-end me-2"}
                           profile={member.profile}
                           sizeMultiplier={0.4}
        />
        <div className={"flex-grow-1"}>
          {actions.map(({ name, datetime }, index) => (<div
            className={"bg-body-tertiary  rounded rounded-3 mt-2 p-2"}
            key={index}
          >
            {index == 0 ? (<div>{`${member.profile.firstName} ${member.profile.lastName}`}</div>) : (<></>)}
            <div className={"mt-1"}>{name} - {datetime}</div>
          </div>))}
        </div>
      </ListGroup.Item>))}
    </ListGroup>
  </>);
}
