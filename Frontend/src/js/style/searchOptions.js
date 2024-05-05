function activateOption(...searchOptions) {
  searchOptions.forEach((option) => {
    option.css({
      backgroundColor: 'var(--color3)',
      borderColor: 'var(--color1)'
    });
  })
}

function deactivateOption(...searchOptions) {
  searchOptions.forEach((option) => {
    option.css({
      backgroundColor: 'white',
      borderColor: 'white'
    });
  })
}

export { activateOption, deactivateOption };
