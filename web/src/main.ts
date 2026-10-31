import {
  sortResults
} from "@/query";

const results = sortResults([{ title: "Demo", score: 0.8 }]);
console.log(results[0]?.title);
