import {useForm} from "react-hook-form";
import Page from "./Page.tsx";
import "../css/Forms.css"
import {signUp} from "../authentication.ts";

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

    function onSubmit(data: IFormInputs) {
        console.log(data);
        signUp(data.login, data.email, data.firstname, data.lastname, data.password).then(() => {
            window.location.href = "/";
        });
    }

    return (
        <Page>
            <div id={"form-back"}>
                <h1> Sign Up</h1>
                <form onSubmit={handleSubmit(onSubmit)} method={"POST"}>
                    <label>
                        Email
                        <input type={"email"}
                               className={"form-field"} {...register("email", {required: "This field is required"})}/>
                        <span>{errors.email?.message}</span>
                    </label>
                    <label>
                        Firstname
                        <input type={"text"}
                               autoComplete={"no"}
                               className={"form-field"} {...register("firstname", {required: "This field is required"})}/>
                        <span>{errors.firstname?.message}</span>
                    </label>
                    <label>
                        Lastname
                        <input type={"text"}
                               autoComplete={"no"}
                               className={"form-field"} {...register("lastname", {required: "This field is required"})}/>
                        <span>{errors.lastname?.message}</span>
                    </label>
                    <label>
                        Login
                        <input type={"text"}
                               autoComplete={"no"}
                               className={"form-field"} {...register("login", {required: "This field is required", minLength: {value: 3, message: "Min length of login is 3"}})}/>
                        <span>{errors.login?.message}</span>
                    </label>
                    <label>
                        Password
                        <input type={"password"}
                               autoComplete={"new-password"}
                               className={"form-field"} {...register(
                            "password", {
                                required: "This field is required",
                                minLength: {"value": 8, message: "Min length must be 8 and more"}
                            }
                        )} />
                        <span>{errors.password?.message}</span>
                    </label>
                    <input type="submit" value={"Submit"}/>
                </form>
            </div>
        </Page>

    );
}