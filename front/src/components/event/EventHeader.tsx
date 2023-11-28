import { IEvent } from "./interfaces.ts";
import { useState } from "react";
import { BsThreeDotsVertical } from "react-icons/bs";
import { Button, Form, Modal } from "react-bootstrap";

export function EventHeader({ event }: { event: IEvent }) {
  const [showDescriptionModal, setShowDescriptionModal] = useState(false);
  const [description, setDescription] = useState(event.description);
  const [newDescription, setNewDescription] = useState<string | null>(null);

  return (<div className={"border border-top-0 rounded-bottom-5 bg-body-tertiary mb-2"}>
    <div className={"d-flex flex-row ps-2 pe-3 py-1"}>
      <div
        className={"border rounded-5 my-1 me-3"}
        style={{
          height: "3.5rem", width: "3.5rem", fontSize: "1.5rem", padding: "0.5rem", textAlign: "center",
        }}
      >
        {parseInt(event.date.slice(8, 10))}
      </div>
      <div className={"flex-grow-1"}>
        <div className={"d-flex flex-column align-items-start"}>
          <div className={"fs-4"}>{description}</div>
          <div
            className={"fs-6"}
          >{`${event.date}, ${event.members.length} members`}</div>
        </div>
      </div>

      <div className={"pt-1 ms-2"}>
        <a
          id={"name-addon"}
          className={"text-body fs-2 hover-cursor-pointer"}
          onClick={() => setShowDescriptionModal(true)}
        >
          <BsThreeDotsVertical />
        </a>
        <Modal
          show={showDescriptionModal}
          onHide={() => setShowDescriptionModal(false)}
        >
          <Modal.Header closeButton>
            <Modal.Title>Description updating</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form>
              <Form.Group
                className="mb-3"
                controlId="exampleForm.ControlTextarea1"
              >
                <Form.Label>New description</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  defaultValue={description}
                  onChange={(e) => {
                    setNewDescription(e.target.value);
                  }}
                />
              </Form.Group>
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <Button
              variant="outline-secondary"
              onClick={() => setShowDescriptionModal(false)}
            >
              Close
            </Button>
            <Button
              id={"btn-modal-ok"}
              variant="primary"
              onClick={() => {
                if (newDescription != description) {
                  console.log(`New description ${newDescription}`);
                  setDescription(newDescription!);
                }
                setShowDescriptionModal(false);
              }}
            >
              Save Changes
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
    </div>
  </div>);
}