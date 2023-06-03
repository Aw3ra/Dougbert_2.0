const TipLink = require('@tiplink/api').TipLink;

function createLink() {
  return TipLink.create().then(tiplink => {
    return tiplink;
  });
}

module.exports = { createLink };