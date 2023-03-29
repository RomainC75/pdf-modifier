const { Schema, model, SchemaTypes } = require("mongoose");

const authorizedUserSchema = new Schema(
  {
    email: {
      type: String,
      unique: true,
      required: true,
    }
  },
  {
    timestamps: true,
  }
);

const AuthorizedUser = model("authorizedUser", authorizedUserSchema);

module.exports = AuthorizedUser;
