#[macro_use] extern crate rocket;

use rocket::time::Date;
use rocket::http::{Status, ContentType};
use rocket::form::{Form, Contextual, FromForm, FromFormField, Context};
use rocket::fs::{FileServer, TempFile, relative};
use rocket::serde::{Serialize, json::{Json, Value, json}};


#[derive(Debug, FromForm)]
struct MyForm<'v> {
    taint: Option<&'v str>,
    id: Option<&'v str>,
}


// NOTE: We use `Contextual` here because we want to collect all submitted form
// fields to re-render forms with submitted values on error. If you have no such
// need, do not use `Contextual`. Use the equivalent of `Form<Submit<'_>>`.
#[post("/", data = "<form>")]
fn index<'r>(form: Form<MyForm>) -> Value {
    json!({
        "form": {
            "taint":form.taint,
            "id":form.id,
        },
    })
}

#[catch(404)]
fn not_found() -> Value {
    json!({
        "status": "error",
        "reason": "Resource was not found."
    })
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![index])
        .register("/json", catchers![not_found])
}
