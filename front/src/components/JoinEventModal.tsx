import "../css/CreateEvent.css";
import getAuthHeader from "../authentication.ts";
import { Button, Form, InputGroup, Modal } from "react-bootstrap";
import { Formik } from "formik";
import * as yup from "yup";
import { URLS } from "../constants.ts";

async function joinEventAPI(inputs: { id: number | string }) {
  console.log(`Create event ${inputs}`);
  const response = await fetch(URLS.join_event(inputs.id), {
    method: "POST",
    headers: getAuthHeader(),
  });
  if (response.ok) {
    const json = await response.json();
    console.log(`Joined, ${JSON.stringify(json)}`);
    return json;
  }
}

export default function JoinEventModal(props: {
  show: boolean;
  onHide: () => void;
}) {
  return (
    <Modal show={props.show} onHide={props.onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Join event</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Formik
          validationSchema={yup.object().shape({
            id: yup.number().required(),
          })}
          onSubmit={(values) => {
            console.log(values);
            joinEventAPI(values).then((json) => {
              window.location.href = `/events/${json.event}`;
            });
          }}
          initialValues={{
            id: "",
          }}
        >
          {({ handleSubmit, handleChange, values, errors }) => (
            <Form noValidate onSubmit={handleSubmit}>
              <Form.Group controlId="validationFormikDescription">
                <Form.Label>Event id</Form.Label>
                <InputGroup hasValidation>
                  <Form.Control
                    type="text"
                    placeholder="12"
                    aria-describedby="inputGroupPrepend"
                    name="id"
                    value={values.id}
                    onChange={handleChange}
                    isInvalid={!!errors.id}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.id}
                  </Form.Control.Feedback>
                </InputGroup>
              </Form.Group>
              <Button type="submit">Join</Button>
            </Form>
          )}
        </Formik>
      </Modal.Body>
    </Modal>
  );
}
