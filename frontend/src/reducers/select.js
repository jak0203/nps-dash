import {SELECT_HAS_CHANGED} from "../actions/select";

const initial_state = {
  product: '',
};

export function productSelect(state = initial_state, { type, payload }) {
  switch (type) {
    case SELECT_HAS_CHANGED:
      return {
        ...state,
        product: payload['value'],
      };
    default:
      return state;
  }
}