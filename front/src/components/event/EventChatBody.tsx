import { IChatElement } from "./interfaces.ts";
import { ListGroup } from "react-bootstrap";
import { RoundedAvatarLink } from "../Profile.tsx";

export function EventChatBody() {
  const chatElements: IChatElement[] = [
    {
      member: {
        profile: {
          id: 1,
          firstName: "User",
          lastName: "1",
        },
      },
      actions: [{ name: "Initialed", datetime: "2023-10-30 12:00:00" }],
    },
    {
      member: {
        profile: {
          id: 2,
          firstName: "User",
          lastName: "2",
        },
      },
      actions: [
        {
          name: "Added money",
          datetime: "2023-10-30 12:01:00",
        },
        {
          name: "Added money",
          datetime: "2023-10-30 12:01:00",
        },
      ],
    },
  ];
  return (
    <>
      <ListGroup variant={"flush"}>
        {chatElements.map(
          (
            chatElement,
            index, // Remove index key
          ) => (
            <ListGroup.Item
              className={"d-flex flex-row border-0 px-2 pb-2"}
              key={index}
            >
              <div className={"m-1 me-3 align-self-end"}>
                <RoundedAvatarLink
                  profile={chatElement.member.profile}
                  sizeMultiplier={0.5}
                />
              </div>
              <div className={"flex-grow-1"}>
                {chatElement.actions.map((action, index) => (
                  <>
                    <div
                      className={"bg-body-tertiary  rounded rounded-3 mt-2 p-2"}
                    >
                      {index == 0 ? (
                        <div>{`${chatElement.member.profile.firstName} ${chatElement.member.profile.lastName}`}</div>
                      ) : (
                        <></>
                      )}
                      {action.name} - {action.datetime}
                    </div>
                  </>
                ))}
              </div>
            </ListGroup.Item>
          ),
        )}
      </ListGroup>
    </>
  );
}
