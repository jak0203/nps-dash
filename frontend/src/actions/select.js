export const PRODUCT_SELECT_HAS_CHANGED = 'PRODUCT_SELECT_HAS_CHANGED';
export const USER_SELECT_HAS_CHANGED = 'USER_SELECT_HAS_CHANGED';

export function selectHandleChange(event) {
  console.log(event.target);
  if (event.target.name === 'product') {
    return {
      type: PRODUCT_SELECT_HAS_CHANGED,
      payload: {
        'value': event.target.value,
      }
    }
  }
  return {
    type: USER_SELECT_HAS_CHANGED,
    payload: {
      'value': event.target.value,
    }
  }
}