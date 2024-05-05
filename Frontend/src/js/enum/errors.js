import { Config } from '../../config'

const FrontendError = {
  emptyField: 'All the required fields must be filled',
  invalidEmail: 'Invalid email',
  invalidUrl: 'Invalid URL',
  fileTooLarge: `File is too large. Max size is ${Config.MAX_TUTORIAL_SIZE} KB.`
}

const BackendError = {
  0: {
    text: 'Unknown error occured.',
    field: []
  },
  1: {
    text: `Username must:
      - be ${Config.MIN_USERNAME_LENGTH}-${Config.MAX_USERNAME_LENGTH} chars
      - contain only digits, letters and "${Config.USERNAME_ALLOWED_CHARS}" symbols
      - not start or end with "${Config.USERNAME_ALLOWED_CHARS}" symbols
      - not start with digits`,
    field: ['username']
  },
  2: {
    text: 'Username already exists.',
    field: ['username']
  },
  3: {
    text: 'Email already exists.',
    field: ['email']
  },
  4: {
    text: `First name must be < ${Config.MAX_NAME_LENGTH} chars and contain only letters.`,
    field: ['firstname']
  },
  5: {
    text: `Last name must be < ${Config.MAX_NAME_LENGTH} chars and contain only letters.`,
    field: ['lastname']
  },
  6: {
    text: `Password must:
      - be ${Config.MIN_PWD_LENGTH}-${Config.MAX_PWD_LENGTH} chars
      - contain at least 2 letters (1 in upper case and 1 in lower case)
      - contain at least 1 digit and 1 special symbol
      - not contain spaces`,
    field: ['password']
  },
  7: {
    text: 'Passwords are not equal.',
    field: ['password', 'passwordConfirm']
  },
  8: {
    text: 'Invalid username or password.',
    field: ['username', 'password']
  },
  9: {
    text: 'This account is not activated. Please check your email.',
    field: []
  },
  10: {
    text: 'Wrong current password.',
    field: ['currentPassword']
  },
  11: {
    text: 'New password must differ from previous one.',
    field: ['currentPassword', 'password']
  },
  // Pay attention that 12-th code is used directly in the code!
  12: {
    text: 'Invalid token.',
    field: []
  },
  13: {
    text: `Title is invalid. Title must be ${Config.MIN_TITLE_LENGTH}-${Config.MAX_TITLE_LENGTH} chars.`,
    field: ['title']
  },
  14: {
    text: `Too many tags. Max number of tags is ${Config.MAX_N_TAGS}`,
    field: ['tags']
  },
  15: {
    text: `Tag must:
      - be ${Config.MIN_TAG_LENGTH}-${Config.MAX_TAG_LENGTH} chars
      - contain only digits, letters and "${Config.TAG_ALLOWED_CHARS}" symbols
      - not contain only "${Config.TAG_ALLOWED_CHARS}" symbols`,
    field: ['tags']
  },
  16: {
    text: `Annotation is invalid. Max annotation length is ${Config.MAX_ANNOTATION_LENGTH} chars.`,
    field: ['annotation']
  },
  17: {
    text: `File is too large. Max allowed file size is ${Math.ceil(Config.MAX_TUTORIAL_SIZE / 1024)} KB.`,
    field: ['file']
  },
  // Pay attention that 18-th code is used directly in the code!
  18: {
    text: 'Content not found.',
    field: []
  }
}

export { FrontendError, BackendError };