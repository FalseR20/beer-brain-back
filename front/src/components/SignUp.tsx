import { signUp } from "../authentication.ts";
import Template from "./Template.tsx";
import { Button, Col, Form, InputGroup, Row } from "react-bootstrap";
import { Formik } from "formik";
import * as yup from "yup";

export default function SignIn() {
  return (
    <Template>
      <div id={"form-back"}>
        <h1> Sign Up</h1>
        <Formik
          validationSchema={yup.object().shape({
            email: yup.string().email().required(),
            firstname: yup.string().required(),
            lastname: yup.string().required(),
            username: yup.string().required(),
            password: yup.string().required().min(8),
            passwordConfirmation: yup
              .string()
              .required()
              .oneOf([yup.ref("password")]),
          })}
          onSubmit={(values, formikHelpers) => {
            console.log(values);
            signUp(
              values.username,
              values.email,
              values.firstname,
              values.lastname,
              values.password,
            ).then((is_success) => {
              if (is_success) {
                window.location.href = "/";
              } else {
                formikHelpers.setSubmitting(false);
                formikHelpers.setFieldError("username", "User already exists");
              }
            });
          }}
          initialValues={{
            email: "",
            firstname: "",
            lastname: "",
            username: "",
            password: "",
            passwordConfirmation: "",
          }}
          // validateOnChange={false}
          // validateOnBlur={false}
        >
          {({ handleSubmit, handleBlur, handleChange, errors }) => (
            <Form noValidate onSubmit={handleSubmit}>
              <Row>
                <Col>
                  <Form.Group controlId="validationFormikFirstname">
                    <Form.Label>Firstname</Form.Label>
                    <InputGroup hasValidation>
                      <Form.Control
                        type="text"
                        placeholder="Firstname"
                        aria-describedby="inputGroupPrepend"
                        name="firstname"
                        onChange={handleChange}
                        onBlur={handleBlur}
                        isInvalid={!!errors.firstname}
                      />
                      <Form.Control.Feedback type="invalid">
                        {errors.firstname}
                      </Form.Control.Feedback>
                    </InputGroup>
                  </Form.Group>
                </Col>
                <Col>
                  <Form.Group controlId="validationFormikLastname">
                    <Form.Label>Lastname</Form.Label>
                    <InputGroup hasValidation>
                      <Form.Control
                        type="text"
                        placeholder="Lastname"
                        aria-describedby="inputGroupPrepend"
                        name="lastname"
                        onChange={handleChange}
                        onBlur={handleBlur}
                        isInvalid={!!errors.lastname}
                      />
                      <Form.Control.Feedback type="invalid">
                        {errors.lastname}
                      </Form.Control.Feedback>
                    </InputGroup>
                  </Form.Group>
                </Col>
              </Row>

              <Form.Group controlId="validationFormikEmail">
                <Form.Label>Email</Form.Label>
                <InputGroup hasValidation>
                  <Form.Control
                    type="email"
                    placeholder="Email"
                    aria-describedby="inputGroupPrepend"
                    name="email"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    isInvalid={!!errors.email}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.email}
                  </Form.Control.Feedback>
                </InputGroup>
              </Form.Group>
              <Form.Group controlId="validationFormikUsername">
                <Form.Label>Username</Form.Label>
                <InputGroup hasValidation>
                  <InputGroup.Text id="basic-addon1">@</InputGroup.Text>
                  <Form.Control
                    type="text"
                    placeholder="Username"
                    aria-describedby="inputGroupPrepend"
                    name="username"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    isInvalid={!!errors.username}
                  />
                  <Form.Control.Feedback type="invalid">
                    {errors.username}
                  </Form.Control.Feedback>
                </InputGroup>
              </Form.Group>
              <Row>
                <Col>
                  <Form.Group controlId="validationFormikPassword">
                    <Form.Label>Password</Form.Label>
                    <InputGroup hasValidation>
                      <Form.Control
                        type="password"
                        placeholder="Password"
                        aria-describedby="inputGroupPrepend"
                        name="password"
                        onChange={handleChange}
                        onBlur={handleBlur}
                        isInvalid={!!errors.password}
                      />
                      <Form.Control.Feedback type="invalid">
                        {errors.password}
                      </Form.Control.Feedback>
                    </InputGroup>
                  </Form.Group>
                </Col>
                <Col>
                  <Form.Group controlId="validationFormikPasswordConfirmation">
                    <Form.Label>Password confirmation</Form.Label>
                    <InputGroup hasValidation>
                      <Form.Control
                        type="password"
                        placeholder="Repeat password"
                        aria-describedby="inputGroupPrepend"
                        name="passwordConfirmation"
                        onChange={handleChange}
                        onBlur={handleBlur}
                        isInvalid={!!errors.passwordConfirmation}
                      />
                      <Form.Control.Feedback type="invalid">
                        {errors.passwordConfirmation}
                      </Form.Control.Feedback>
                    </InputGroup>
                  </Form.Group>
                </Col>
              </Row>
              <Button type="submit">Submit</Button>
            </Form>
          )}
        </Formik>
      </div>
    </Template>
  );
}
