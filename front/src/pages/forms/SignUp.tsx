import {useForm} from "react-hook-form";
import Page from "../../components/Page.tsx";
import "./Forms.css"
import {useState} from "react";
import {signUp} from "../../auth/authentication.ts";

interface IFormInputs {
    login: string
    email: string
    firstname: string
    lastname: string
    password: string
}


export default function SignUp() {
    const {
        register,
        handleSubmit,
        formState: {errors},
    } = useForm<IFormInputs>();

    const [submitButtonText, setSubmitButtonText] = useState("Submit")

    function onSubmit(data: IFormInputs) {
        console.log(data);
        setSubmitButtonText("...")
        signUp(data.login, data.email, data.firstname, data.lastname, data.password).then(r => r);
        setTimeout(() => {
            setSubmitButtonText("Submit")
        }, 500)
    }

    return (
        <Page>
            <div id={"form-back"}>
                <h1> Sign Up</h1>
                <form onSubmit={handleSubmit(onSubmit)} method={"POST"}>
                    <label>
                        Login
                        <input type={"text"}
                               className={"form-field"} {...register("login", {required: "This field is required", minLength: {value: 3, message: "Min length of login is 3"}})}/>
                        <span>{errors.login?.message}</span>
                    </label>
                    <label>
                        Email
                        <input type={"email"}
                               className={"form-field"} {...register("email", {required: "This field is required"})}/>
                        <span>{errors.email?.message}</span>
                    </label>
                    <label>
                        Firstname
                        <input type={"text"}
                               className={"form-field"} {...register("firstname", {required: "This field is required"})}/>
                        <span>{errors.firstname?.message}</span>
                    </label>
                    <label>
                        Lastname
                        <input type={"text"}
                               className={"form-field"} {...register("lastname", {required: "This field is required"})}/>
                        <span>{errors.lastname?.message}</span>
                    </label>
                    <label>
                        Password
                        <input type={"password"}
                               className={"form-field"} {...register(
                            "password", {
                                required: "This field is required",
                                minLength: {"value": 8, message: "Min length must be 8 and more"}
                            }
                        )} />
                        <span>{errors.password?.message}</span>
                    </label>
                    <input type="submit" value={submitButtonText}/>
                </form>
            </div>
        </Page>

    );
}