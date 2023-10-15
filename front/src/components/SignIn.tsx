import Template from "./Template.tsx";
import { Button, Form, InputGroup } from "react-bootstrap";
import { signIn } from "../authentication.ts";
import { Formik } from "formik";
import * as yup from "yup";

export default function SignIn() {
  return (
    <Template>
      <div id={"form-back"}>
        <h1> Sign In</h1>
        <Formik
          validationSchema={yup.object().shape({
            username: yup.string().required(),
            password: yup.string().required(),
          })}
          onSubmit={(values, formikHelpers) => {
            console.log(values);
            signIn(values.username, values.password).then((is_success) => {
              if (is_success) {
                window.location.href = "/";
              } else {
                formikHelpers.setSubmitting(false);
                const message = "Wrong password or login";
                formikHelpers.setFieldError("username", message);
                formikHelpers.setFieldError("password", message);
              }
            });
          }}
          initialValues={{
            username: "",
            password: "",
          }}
        >
          {({ handleSubmit, handleChange, values, errors }) => (
            <Form noValidate onSubmit={handleSubmit}>
              <Form.Group controlId="validationFormikUsername">
                <Form.Label>Username</Form.Label>
                <InputGroup hasValidation>
                  <Form.Control
                    type="text"
                    placeholder="Username"
                    aria-describedby="inputGroupPrepend"
                    name="username"
                    value={values.username}
                    onChange={handleChange}
                    isInvalid={!!errors.username}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.username}
                  </Form.Control.Feedback>
                </InputGroup>
              </Form.Group>
              <Form.Group controlId="validationFormikPassword">
                <Form.Label>Password</Form.Label>
                <InputGroup hasValidation>
                  <Form.Control
                    type="password"
                    placeholder="Password"
                    aria-describedby="inputGroupPrepend"
                    name="password"
                    value={values.password}
                    onChange={handleChange}
                    isInvalid={!!errors.password}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.password}
                  </Form.Control.Feedback>
                </InputGroup>
              </Form.Group>
              <Button type="submit">Submit</Button>
            </Form>
          )}
        </Formik>
      </div>
    </Template>
  );
}
