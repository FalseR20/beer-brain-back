import {useForm} from "react-hook-form";
import Page from "../components/Page.tsx";
import "./Forms.css"
import {useState} from "react";
import {signIn} from "../auth/authentication.ts";

interface IFormInputs {
    user: string
    password: string
}


export default function SignIn() {
    const {
        register,
        handleSubmit,
        formState: {errors},
    } = useForm<IFormInputs>();

    const [submitButtonText, setSubmitButtonText] = useState("Submit")

    function onSubmit(data: IFormInputs) {
        console.log(data);
        setSubmitButtonText("...")
        signIn(data.user, data.password).then(r => r);
        setTimeout(() => {setSubmitButtonText("Submit")}, 500)
    }

    return (
        <Page>
            <div id={"form-back"}>
                <h1> Sign In</h1>
                <form onSubmit={handleSubmit(onSubmit)} method={"POST"}>
                    {/* register your input into the hook by invoking the "register" function */}
                    <label>
                        Email or login
                        <input type={"text"}
                               className={"form-field"} {...register("user", {required: "This field is required"})}/>
                        <span>{errors.user?.message}</span>

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