import Page from "./Page.tsx";
import { ReactNode, useEffect, useState } from "react";
import getAuthHeader from "../authentication.ts";
import { Button, Card, Col, Row } from "react-bootstrap";

interface DebtJSON {
  id: number,
  members_count: number,
  date: string,
  description: string,
  is_closed: boolean
}

export default function Home() {
  return <Page isAuthRequired={true}>
    <div className={"d-flex justify-content-between my-4"}>
      <span className={"fs-1"}>All debts</span>
      <div className={"d-flex flex-row-reverse"}>
        <Button className={"fs-3 ms-4"} variant={"success"} size={"lg"} href={"/create_event"}>Create
          event</Button>
        <Button className={"fs-3"} variant={"outline-success  "} size={"lg"} href={"/join_event"}>Join event</Button>
      </div>
    </div>
    <Debts />
  </Page>;
}

function Debts(): ReactNode {
  const [debts, setDebts] = useState<DebtJSON[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/core/common-events/", {
      headers: getAuthHeader(),
    }).then(response => response.json())
      .then(data => setDebts(data));
  }, []);

  return (<Row xs={1} md={2} className={"g-3"}>
      {debts.map((debt => (<Col key={`Debt${debt.id}`}>
        <Card className={"p-0"} border={debt.is_closed ? "secondary" : "primary"}>
          <Card.Header>
            <Row>
              <Col>
                <span>{debt.date}</span>
              </Col>
              <Col>
                <span className={"text-end"}>{}</span>
              </Col>
            </Row>
          </Card.Header>
          <Card.Body>
            <Card.Title>{debt.description}</Card.Title>
            <Card.Text>{debt.members_count} members</Card.Text>
            <Row className={"mx-0"}>
              <Button variant={"primary"} size={"lg"} href={`/events/${debt.id}/`}>Look</Button>
            </Row>
          </Card.Body>
        </Card>
      </Col>)))}
    </Row>

  );
}
