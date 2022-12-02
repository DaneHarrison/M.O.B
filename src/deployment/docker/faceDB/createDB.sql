create table "UserFaces"
(
    "userID"     serial,
    "userName"   text  not null,
    "userWeight" double precision[],
    "userPhoto"  bytea not null,
    primary key ("userID")
);

alter table "UserFaces"
    owner to "user";

DROP FUNCTION IF EXISTS find_min;
DROP TYPE IF EXISTS db_answer;

CREATE EXTENSION plpython3u;
CREATE TYPE db_answer AS (
    idx int,
    distance float
);

CREATE FUNCTION find_min(aa float[]) RETURNS db_answer AS $$
import math
my_idx = -1
my_distance = 0
my_mins = []
weights = plpy.execute("SELECT * FROM public.\"UserFaces\"")
for i in range(len(weights)):
    curr_weight = weights[i]['userWeight']
    tmp_hold = []
    for j in range(len(curr_weight)):
        tmp_hold.append(curr_weight[j] - aa[j])
    tmp_hold = [x**2 for x in tmp_hold]
    my_sum = sum(tmp_hold)
    my_mins.append(math.sqrt(my_sum))
my_distance = min(my_mins)
my_idx = my_mins.index(my_distance)
return (my_idx,my_distance)
$$ LANGUAGE plpython3u;