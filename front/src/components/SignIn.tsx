import {useForm} from "react-hook-form";
import Page from "./Page.tsx";
import "../css/Forms.css"
import {signIn} from "../authentication.ts";

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
    function onSubmit(data: IFormInputs) {
        console.log(data);
        signIn(data.user, data.password).then(() => {
            window.location.href = "/";
        });
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
                               autoComplete={"current-password"}
                               className={"form-field"} {...register(
                            "password", {
                                required: "This field is required",
                                minLength: {"value": 8, message: "Min length must be 8 and more"},
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