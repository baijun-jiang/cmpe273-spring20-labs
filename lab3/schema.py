from ariadne import gql, load_schema_from_path

schema = gql(
    """
    type Student {
        name: String!
        id: Int!
    },
    type Class {
        id: Int!
        name: String!
        students: [Studnet]!
    }
    """
)