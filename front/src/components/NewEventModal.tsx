import "../css/CreateEvent.css";
import getAuthHeader from "../authentication.ts";
import { Button, Form, InputGroup, Modal } from "react-bootstrap";
import { Formik } from "formik";
import * as yup from "yup";
import { URLS } from "../constants.ts";

async function createEventAPI(inputs: { description: string }) {
  console.log(`Create event ${inputs}`);
  const formData = new FormData();
  formData.append("description", inputs.description);
  const response = await fetch(URLS.create_event, {
    method: "POST",
    headers: getAuthHeader(),
    body: formData,
  });
  if (response.ok) {
    const json = await response.json();
    console.log(`Created, ${JSON.stringify(json)}`);
    return json;
  }
}

export default function NewEventModal(props: {
  show: boolean;
  onHide: () => void;
}) {
  return (
    <Modal show={props.show} onHide={props.onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Create event</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Formik
          validationSchema={yup.object().shape({
            description: yup.string().required(),
          })}
          onSubmit={(values) => {
            console.log(values);
            createEventAPI(values).then((json) => {
              window.location.href = `/events/${json.id}`;
            });
          }}
          initialValues={{
            description: "",
          }}
        >
          {({ handleSubmit, handleChange, values, errors }) => (
            <Form noValidate onSubmit={handleSubmit}>
              <Form.Group controlId="validationFormikDescription">
                <Form.Label>Description</Form.Label>
                <InputGroup hasValidation>
                  <Form.Control
                    type="text"
                    placeholder="Chill-Out"
                    aria-describedby="inputGroupPrepend"
                    name="description"
                    value={values.description}
                    onChange={handleChange}
                    isInvalid={!!errors.description}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.description}
                  </Form.Control.Feedback>
                </InputGroup>
              </Form.Group>
              <Button type="submit">Create</Button>
            </Form>
          )}
        </Formik>
      </Modal.Body>
    </Modal>
  );
}
