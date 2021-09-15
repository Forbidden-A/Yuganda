module default {

    type StarredMessage {
        required property message_id -> int64;
        required property followup_id -> int64;
        required property stars -> int32;
    }

}
