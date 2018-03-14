
export const SELECT_HAS_CHANGED = 'SELECT_HAS_CHANGED';

export function selectHandleChange(event) {
  return {
    type: SELECT_HAS_CHANGED,
    payload: {
      'value': event.target.value,
      'name': event.target.name
    }
  }
}