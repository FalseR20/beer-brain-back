import { IEvent } from "./interfaces.ts";
import { Button, ListGroup } from "react-bootstrap";

export function EventPayers({ event }: { event: IEvent }) {
  const membersWithDeposits = event.members.filter((member) => member.deposits.length > 0);
  return (<>
    <div className={"d-flex justify-content-between align-items-center"}>
      <h2 className={"my-3"}>Payers</h2>
      <Button variant={"success"}>Add payment</Button>
    </div>
    <div className={"border border-secondary rounded-3 p-2"}>
      <ListGroup className={""} variant={"flush"}>
        {membersWithDeposits.length > 0 ? (event.members.map((member) => member.deposits.map((deposit) => (
          <ListGroup.Item key={deposit.id}>
                  <span>
                    {deposit.description} for {deposit.value}
                  </span>
          </ListGroup.Item>)))) : (<ListGroup.Item>
          <span>Nothing</span>
        </ListGroup.Item>)}
      </ListGroup>
    </div>
  </>);
}