> # Testing Report (Pigeonhole)

Revision History:

<style>#rev +table td:nth-child(1) { white-space: nowrap }</style>
<div id="rev"></div>

| Date   | Author | Description |
| ------ | ------ | ----------- |
| Apr 20 | Ciel ZHAO | Converted the template |
| Apr 24 | Xiaoquan Xu | Provided the first three parts of Pigeonhole's testing plan |
| Apr 26 | Xiaoquan Xu | Provided the last part of Pigeonhole's testing plan |
| May 04 | Xiaoquan Xu | Finished testing Pigeonhole's cloud-platform |

[toc]
 
## Introduction

### Intended Audience and Purpose

This document provides the testing method and results, corresponding to the requirement from the customer. It consists of 3 parts, the testing cases, the test plan, and the testing results.


### How to use the document

You may refer to the content section for the structure of the document, in which Sec. Testing Cases collect the unit and module test information from each team; Sec. Testing Plan shows the steps and expected results of the integration test; Sec. Results describes the real world data out of the test, and the correspondence to the requirements.

![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba5481.png)

## Testing Cases

<!--
In this section, each team propose their testing cases on unit and module testing.
-->

- Unit testing considers checking a single component of the system.
- Module testing considers checking overlap modules in the system.

### Server

#### Authentication

##### Test 1.Request a cloud-signed time stamp

- [x] Use `GET /timestamp` to generate a signed timestamp.

> Like `1650983735:6bce5953a9506d6c14f2522fd6228afbee394da3
`
- [x] Two requests at different time should return different values.

:::info
If two requests were sent within a second, it will return the same value.
:::

- [x] If two requests are sent to the same server, the part of their timestamp after the colon should be the same.
- [x] A signed timestamp should be successfully split by a colon.

> For example: `1650375337:6bce5953a9506d6c14f2522fd6228afbee394da3`

- [x] The signed timestamp should be valid for only 1 hour.

- [x] It should always return 200.

#### Device Management

##### Test 2.Set the contact email

- [x] After sending `POST /device/<uuid>/email`, the contact email should be set.
- [x] If set email for a device which has already been set, the contact email should be updated.
- [x] If the UUID is not a valid UUIDv4, it should return 404.

> UUIDv4 such like `11bf5b37-e0b8-42e0-8dcf-dc8c4aefc000`

:::success
~~It returns 404~~
:::

> The request must be of type `application/json`. Example request:
> ```
> {
>     "email": "t@t.tt"
> }
> ```

> The email must be of the right form and a maximum of 254 characters.

- [x] If either the form of request or `email` is invalid, it should return 400.

> Although the domain name `c.dev` does not exist, `pigeonhoe@c.dev` is a valid email here. 

> `hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhole11111111111111@ciel.dev
` is not valid because the number of characters before `@` exceeds 64.

- [x] If both the forms of request and `email` is valid, it should return 200.

> `pigeonhole@ciel.dev` and `t@t.tt` are valid

##### Test 3.Get the contact email

- [x] After sending `GET /device/<uuid>/email`, the contact email should be get.
- [x] If the contact email was not set, it should return 404.
- [x] If the contact email was get, it should return 200.
- [x] The response should be of the same right form as the request in Test 2.

##### Test 4.Clear the contact email setting

- [x] After sending `DELETE /device/<uuid>/email`, the contact email setting should be cleared.
- [x] It should always return 200. Even if the contact email was not set.

##### Test 5.Check whether calibration data is available

- [x] Send `HEAD /device/<uuid>/calibration` to check.
- [x] If the data is not found, it should return 404.
- [x] If the data is found available, it should return 200.

##### Test 6.Upload new calibration data to the cloud platform

- [x] After sending `PUT /device/<uuid>/calibration`, the new calibration data should be uploaded.

> The request should be of type `multipart/form-data` with a file field `caxibration`, the file must be of type `application/x-tar+gzip`.

- [x] If the request is not valid, it should return 400.
- [x] If the `Signature` is not valid, it should return 400.
- [x] If the data was uploaded successfully, it should return 200.

##### Test 7.Clear calibration data from the cloud

- [x] After sending `DELETE /device/<uuid>/calibration`, the calibration data from the cloud should be cleared.
- [x] It should always return 200.

##### Test 8.Check the version of the device model on the server

- [x] Send `HEAD /device/<uuid>/model` to check.
- [x] If the device model does exist, the response should contain a `Last-Modified` header of the device model.
- [x] If the device model does not exist, the response should not contain `Last-Modified`. But the base version is still available to download.
- [x] The response should contain a `Content-Length` header to indicate the size of model.
- [x] It should always return 200.

##### Test 9.Acquire the current version of the device model

- [x] After sending `GET /device/<uuid>/model`, the current version of the device model should be get, signed with the platform key.
- [x] If the device model does not exist, the base version should be provided.
- [x] The response should be of type `application/octet-stream`, and have a `Signature` header to be passed to the device.
- [x] It should always return 200.

##### Test 10.Clear device model from the cloud

- [x] After sending `DELETE /device/<uuid>/model`, the device model from the cloud should be cleared.
- [x] It should always return 200.

#### Administration

##### Test 11.Download the calibration data from the cloud

- [x] After sending `GET /device/<uuid>/calibration`, the calibration data from the cloud should be downloaded.
- [x] If no data is collected, it should return 404.
- [x] If downloaded successfully, it should return 200.
- [x] The response should be of type `application/x-tar+gzip`.
- [x] If the request is sent by device but not manager, it should return 403.

##### Test 12.Upload a new model to the cloud

- [x] After sending `PUT /device/<uuid>/model`, a new model should be uploaded to the cloud.

> The request should be of type `multipart/form-data` with a file field `model`.

- [x] If the request is invalid, it should return 400.
- [x] If uploaded successfully, it should return 200.
- [x] If the request is sent by device but not manager, it should return 403.

##### Test 13.Delete everything specified from the cloud

- [x] After sending `DELETE /device/<uuid>`, everything of the specified device from the cloud should be deleted, and we'd also selectively prohibit its future use of the cloud platform.

> The request must be of type `application/json`. Example request:
> ```
> {
>     "ban": true // disable cloud functionalities for this device
> }
> ```

- [x] If the request is invalid, it should return 400.
- [x] If deleted successfully, it should return 200.

##### Test 14.Log in to the current session

- [x] Use `POST /session` to log in to the current session.

> The request must be of type `application/json`. Example request:
> ```
> {
>     "username": "UserName",
>     "password": "PaSSw0Rd!"
> }
> ```

- [x] If the request is in invalid form, it should return 400.
- [x] If the username or the password is wrong，it should return 403 and do nothing.
- [x] If the username and the password match correctly, it should return 200 and set a new session.

##### Test 15.Log out

- [x] Use `DELETE /session` to log out.
- [x] If log out without logging in, it should do nothing.
- [x] It should always return 200.

##### Test 16.Set a default model to the cloud

- [x] After sending `PUT /model/base`, a model should be uploaded to the cloud to be set as the default model for users without calibration.
> The request should be of type `multipart/form-data` with a file field `model`.
- [x] If the request is invalid, it should return 400.
- [x] If uploaded successfully, it should return 200.

#### Device API

##### Test 17.Confirm the link is established

:::info
return 404 NOT FOUND
:::

- [ ] Use `HEAD /` to check authentication.
- [ ] It should always return `200 OK` to confirm the link is established.

##### Test 18.Provide status information

- [ ] Use `GET /` to provide the client with status information of the device.
- [ ] The response should be of type `application/json`.

> Example response with comments:
> ```
> {
>     "id": "00000000-0000-0000-0000-000000000000", // string, the device UUID
>     "battery": 90, // int, percentage of battery
>     "charging": true, // bool, true if power connected
>     "prediction": "walk", // string, the current detected motion
> }
> ```

- [ ] It should always return `200 OK` to confirm the link is established.

##### Test 19.Obtain a signed device ticket

- [ ] After sending `GET /ticket?ts=<server_timestamp>`, if the timestamp is of the right shape, the device signs it with the device key to creating and returns a device ticket.

> The `server_timestamp` is from the `/timestamp` API of the cloud platform.

- [ ] If the timestamp is missing or malformed, it should return 400.
- [ ] If the timestamp is of the right shape, it should return 200.

##### Test 20.Download the current model from the device

- [ ] After sending `GET /model`, the current model from the device should be downloaded.
- [ ] This API is for debugging only，it should not be called by other procedures.
- [ ] The response should be of type `application/octet-stream`.
- [ ] If there’s currently no model, it should return 404.
- [ ] If downloaded successfully, it should return 200.


##### Test 21.Upload a new model to the device

- [ ] After sending `PUT /model`, a new model should be uploaded to the device.

>The request must have a valid `Signature` header passed from the server.
>The request should be of type `multipart/form-data` with a file field `model`.

- [ ] If the signature is not valid, it should return 400.
- [ ] If uploaded successfully, it should return 200.

##### Test 22.Get metadata of pending calibrations

- [ ] Use `GET /calibration/pending` to get metadata of pending calibrations.
- [ ] If all calibrations are finished, it should return `[]`.
- [ ] The response should be of type `application/json`.

> Example response with comments:
> ```
> [
>     {
>         "name": "walk", // the motion name, [a-z]+
>         "duration": 20, // the duration of recording requested
>         "display": "walk", // the displayed name of motion
>         "desc": "Please walk on a firm and level ground" // the displayed description of motion
>     },
>     // .....
> ]
> ```

- [ ] It should always return 200.

##### Test 23.Initialize a new calibration data recording

- [ ] Use `POST /calibration/<motion>` to initialize a new calibration data recording.

> The `motion` should be from the request above.

- [ ] If the motion name is invalid, it should return 400.
- [ ] If the previous calibration is not finished, it should return 409.
- [ ] If the data recording is able to be initialized, it should return 200 and start the process.

##### Test 24.Acquire all current calibration data

- [ ] Use `GET /calibration` to acquire a pack of all current calibration data, signed with the device key.
- [ ] The response should be of type `application/x-tar+gzip` and have a `Signature` header to be passed to the cloud platform.
- [ ] If no data is collected, it should return 404.
- [ ] If the request is satisfied, it should return 200.

##### Test 25.Clear local calibration data

- [ ] After sending `DELETE /calibration`, the local calibration data should be cleared.
- [ ] It should always return 200.
