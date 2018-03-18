import {USER_SELECT_HAS_CHANGED, PRODUCT_SELECT_HAS_CHANGED, SURVEY_SELECT_HAS_CHANGED} from "../actions/select";

const initial_state = {
  product: '',
  user_type:'all',
  survey: '2018 February'
};

export function dataSelect(state = initial_state, { type, payload }) {
  switch (type) {
    case PRODUCT_SELECT_HAS_CHANGED:
      return {
        ...state,
        product: payload['value'],
      };
      case USER_SELECT_HAS_CHANGED:
      return {
        ...state,
        user_type: payload['value'],
      };
    case SURVEY_SELECT_HAS_CHANGED:
      return {
        ...state,
        survey: payload['value'],
      };
    default:
      return state;
  }
}